from datetime import datetime
from pathlib import Path

from airflow.sdk import dag, task


OUTPUT_DIR = Path("/tmp/projeto-2/extract/output")
BUCKET = "cloud-data-engineering-raw-tony"
GCS_PREFIX = "raw"


@dag(
    dag_id="pipeline_cloud",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["gcp", "data-engineering"],
)
def pipeline_cloud():

    @task
    def extrair_postgres():
        import sys

        from airflow.providers.postgres.hooks.postgres import PostgresHook

        sys.path.append("/usr/local/airflow/include")

        from extract_postgres import extract_with_connection

        hook = PostgresHook(postgres_conn_id="postgres_oltp")
        connection = hook.get_conn()

        try:
            extract_with_connection(connection)
        finally:
            connection.close()

    @task
    def upload_gcs():
        from airflow.providers.google.cloud.hooks.gcs import GCSHook

        hook = GCSHook()

        arquivos = list(OUTPUT_DIR.glob("*.parquet"))

        if not arquivos:
            raise FileNotFoundError(
                f"Nenhum arquivo Parquet encontrado em {OUTPUT_DIR}"
            )

        for arquivo in arquivos:
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

    extracao = extrair_postgres()
    upload = upload_gcs()

    extracao >> upload


pipeline_cloud()
