from datetime import datetime
from pathlib import Path

from airflow.sdk import dag, task


BUCKET = "cloud-data-engineering-raw-tony"
GCS_PREFIX = "raw/metas"


@dag(
    dag_id="load_metas",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["gcp", "json", "metas"],
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

    arquivo = extrair_metas()
    upload_gcs(arquivo)


load_metas()
