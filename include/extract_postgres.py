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

def extract_with_connection(connection):
    cursor = connection.cursor()

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

            print(
                f"{table}: "
                f"{len(dataframe)} registros "
                f"-> {file_path}"
            )
    finally:
        cursor.close()

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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = OUTPUT_DIR / f"{table}_{timestamp}.parquet"

    dataframe.to_parquet(
        file_path,
        engine="pyarrow",
        index=False,
    )

    return file_path


def main():
    if not DB_CONFIG["password"]:
        raise ValueError(
            "A variável de ambiente OLTP_PASSWORD não está definida."
        )

    connection = get_connection()
    cursor = connection.cursor()

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

            print(
                f"{table}: "
                f"{len(dataframe)} registros "
                f"-> {file_path}"
            )

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
