from datetime import datetime
from pathlib import Path

from airflow.sdk import dag, task

import sys
sys.path.append('/usr/local/airflow/include')

from notifications import notify_success, notify_failure


BUCKET = "cloud-data-engineering-raw-tony"
GCS_PREFIX = "raw/metas"
PROJECT_ID = "project-c3b69582-833e-4e2a-88c"
DATASET = "bronze"
TABLE_ID = f"{PROJECT_ID}.{DATASET}.metas_vendas"


@dag(
    dag_id="load_metas",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["gcp", "json", "metas", "bronze"],
    on_success_callback=notify_success,
    on_failure_callback=notify_failure,
)
def load_metas():

    @task
    def extrair_metas():
        import sys

        sys.path.append("/usr/local/airflow/include")

        from extract_metas import extract_metas

        return extract_metas()

    @task
    def upload_gcs(arquivo):
        from airflow.providers.google.cloud.hooks.gcs import GCSHook

        arquivo = Path(arquivo)
        hook = GCSHook()

        destino = f"{GCS_PREFIX}/{arquivo.name}"

        hook.upload(
            bucket_name=BUCKET,
            object_name=destino,
            filename=str(arquivo),
        )

        print(
            f"Upload realizado: {arquivo.name} -> "
            f"gs://{BUCKET}/{destino}"
        )

        return destino

    @task
    def carregar_bronze(destino):
        from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
        from google.cloud import bigquery

        hook = BigQueryHook(
            gcp_conn_id="google_cloud_default",
            use_legacy_sql=False,
        )

        client = hook.get_client(
            project_id=PROJECT_ID,
            location="southamerica-east1",
        )

        uri = f"gs://{BUCKET}/{destino}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            autodetect=True,
        )

        load_job = client.load_table_from_uri(
            uri,
            TABLE_ID,
            job_config=job_config,
        )

        load_job.result()

        print(
            f"Bronze carregado: {uri} -> {TABLE_ID}"
        )

    arquivo = extrair_metas()
    destino = upload_gcs(arquivo)
    carregar_bronze(destino)


load_metas()
