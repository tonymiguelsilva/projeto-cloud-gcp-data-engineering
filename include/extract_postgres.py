import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import psycopg2


TABLES = [
    "clientes",
    "produtos",
    "pedidos",
    "itens_pedido",
]

DB_CONFIG = {
    "host": os.getenv("OLTP_HOST", "localhost"),
    "port": 5432,
    "database": "oltp",
    "user": "oltp_user",
    "password": os.getenv("OLTP_PASSWORD"),
}

OUTPUT_DIR = Path("/tmp/projeto-2/extract/output")


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_watermark(cursor, table):
    cursor.execute(
        """
        SELECT ultima_atualizacao
        FROM pipeline_control
        WHERE tabela_origem = %s
        """,
        (table,),
    )

    result = cursor.fetchone()

    if result is None:
        raise ValueError(
            f"Watermark não encontrado para a tabela {table}"
        )

    return result[0]


def extract_table(cursor, table, watermark):
    cursor.execute(
        f"""
        SELECT *
        FROM {table}
        WHERE updated_at > %s
        ORDER BY updated_at
        """,
        (watermark,),
    )

    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    return pd.DataFrame(rows, columns=columns)


def save_parquet(table, dataframe):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for coluna in dataframe.select_dtypes(include=["datetime64[ns]"]).columns:
        dataframe[coluna] = dataframe[coluna].astype("datetime64[us]")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUT_DIR / f"{table}_{timestamp}.parquet"

    dataframe.to_parquet(
        file_path,
        engine="pyarrow",
        index=False,
    )

    return file_path


def extract_with_connection(connection):
    cursor = connection.cursor()
    arquivos = []

    try:
        for table in TABLES:
            watermark = get_watermark(cursor, table)

            dataframe = extract_table(
                cursor,
                table,
                watermark,
            )

            file_path = save_parquet(
                table,
                dataframe,
            )

            arquivos.append(str(file_path))

            print(
                f"{table}: "
                f"{len(dataframe)} registros "
                f"-> {file_path}"
            )

    finally:
        cursor.close()

    return arquivos


if __name__ == "__main__":
    if not DB_CONFIG["password"]:
        raise ValueError(
            "A variável de ambiente OLTP_PASSWORD não está definida."
        )

    connection = get_connection()

    try:
        arquivos = extract_with_connection(connection)

        for arquivo in arquivos:
            print(f"Arquivo gerado: {arquivo}")

    finally:
        connection.close()
