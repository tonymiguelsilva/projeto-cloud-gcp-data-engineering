from datetime import datetime

from airflow.sdk import dag, task


BUCKET = "cloud-data-engineering-raw-tony"
DATASET = "bronze"
PROJECT_ID = "project-c3b69582-833e-4e2a-88c"

SNAPSHOT = "20260922_153027"

TABLES = [
    "clientes",
    "produtos",
    "pedidos",
    "itens_pedido",
]


@dag(
    dag_id="load_bronze",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["gcp", "bigquery", "bronze"],
)
def load_bronze():

    @task
    def carregar_bronze():
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

        for table in TABLES:
            uri = (
                f"gs://{BUCKET}/raw/"
                f"{table}_{SNAPSHOT}.parquet"
            )

            table_id = f"{PROJECT_ID}.{DATASET}.{table}"

            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.PARQUET,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                autodetect=True,
            )

            load_job = client.load_table_from_uri(
                uri,
                table_id,
                job_config=job_config,
            )

            load_job.result()

            print(
                f"Bronze carregado: {uri} -> {table_id}"
            )


    carregar_bronze()


load_bronze()
