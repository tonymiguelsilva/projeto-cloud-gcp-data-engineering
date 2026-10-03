import json
from datetime import datetime
from pathlib import Path


OUTPUT_DIR = Path("/tmp/projeto-2/extract/metas")

METAS = [
    {"mes": "2026-01", "meta_vendas": 18200000},
    {"mes": "2026-02", "meta_vendas": 17800000},
    {"mes": "2026-03", "meta_vendas": 19200000},
    {"mes": "2026-04", "meta_vendas": 17900000},
    {"mes": "2026-05", "meta_vendas": 18800000},
    {"mes": "2026-06", "meta_vendas": 18500000},
    {"mes": "2026-07", "meta_vendas": 19300000},
    {"mes": "2026-08", "meta_vendas": 18700000},
    {"mes": "2026-09", "meta_vendas": 19600000},
    {"mes": "2026-10", "meta_vendas": 19000000},
    {"mes": "2026-11", "meta_vendas": 20000000},
    {"mes": "2026-12", "meta_vendas": 20500000},
]


def extract_metas():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUT_DIR / f"metas_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as arquivo:
        for meta in METAS:
            arquivo.write(json.dumps(meta, ensure_ascii=False) + "\n")

    print(f"Metas extraídas: {file_path}")

    return str(file_path)


if __name__ == "__main__":
    extract_metas()
