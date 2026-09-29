from datetime import datetime
from pathlib import Path

from airflow.sdk import dag, task


BUCKET = "cloud-data-engineering-raw-tony"
GCS_PREFIX = "raw/weather"


@dag(
    dag_id="load_weather",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["gcp", "api", "weather"],
)
def load_weather():

    @task
    def extrair_weather():
        import sys

        sys.path.append("/usr/local/airflow/include")

        from extract_weather import extract_weather

        return extract_weather()

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

    arquivo = extrair_weather()
    upload_gcs(arquivo)


load_weather()
