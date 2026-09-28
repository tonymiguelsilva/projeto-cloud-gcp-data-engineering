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
            return extract_with_connection(connection)
        finally:
            connection.close()

    @task
    def upload_gcs(arquivos):
        from airflow.providers.google.cloud.hooks.gcs import GCSHook

        hook = GCSHook()

        if not arquivos:
            raise FileNotFoundError(
                "Nenhum arquivo Parquet foi gerado pela extração."
            )

        for arquivo in arquivos:
            arquivo = Path(arquivo)
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

        return arquivos

    @task
    def atualizar_watermark(arquivos):
        import pandas as pd
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        hook = PostgresHook(postgres_conn_id="postgres_oltp")
        connection = hook.get_conn()
        cursor = connection.cursor()

        try:
            for arquivo in arquivos:
                arquivo = Path(arquivo)
                tabela = next(
                    (
                        t
                        for t in [
                            "clientes",
                            "produtos",
                            "pedidos",
                            "itens_pedido",
                        ]
                        if arquivo.name.startswith(f"{t}_")
                    ),
                    None,
                )

                if tabela is None:
                    raise ValueError(
                        f"Tabela não identificada no arquivo: {arquivo.name}"
                    )

                dataframe = pd.read_parquet(arquivo)

                registros = len(dataframe)

                if registros > 0:
                    max_updated_at = dataframe["updated_at"].max()

                    cursor.execute(
                        """
                        UPDATE pipeline_control
                        SET
                            ultima_atualizacao = %s,
                            ultima_execucao = CURRENT_TIMESTAMP,
                            status = 'SUCESSO',
                            registros_processados = %s
                        WHERE tabela_origem = %s
                        """,
                        (
                            max_updated_at.to_pydatetime(),
                            registros,
                            tabela,
                        ),
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE pipeline_control
                        SET
                            ultima_execucao = CURRENT_TIMESTAMP,
                            status = 'SUCESSO',
                            registros_processados = 0
                        WHERE tabela_origem = %s
                        """,
                        (tabela,),
                    )

                print(
                    f"Watermark atualizado: {tabela} | "
                    f"registros={registros}"
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    extracao = extrair_postgres()
    upload = upload_gcs(extracao)
    watermark = atualizar_watermark(upload)

    extracao >> upload >> watermark


pipeline_cloud()
