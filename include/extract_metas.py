import json
from datetime import datetime
from pathlib import Path


OUTPUT_DIR = Path("/tmp/projeto-2/extract/metas")

METAS = [
    {"mes": "2026-01", "meta_vendas": 420000},
    {"mes": "2026-02", "meta_vendas": 430000},
    {"mes": "2026-03", "meta_vendas": 450000},
    {"mes": "2026-04", "meta_vendas": 460000},
    {"mes": "2026-05", "meta_vendas": 470000},
    {"mes": "2026-06", "meta_vendas": 480000},
    {"mes": "2026-07", "meta_vendas": 500000},
    {"mes": "2026-08", "meta_vendas": 510000},
    {"mes": "2026-09", "meta_vendas": 520000},
    {"mes": "2026-10", "meta_vendas": 530000},
    {"mes": "2026-11", "meta_vendas": 550000},
    {"mes": "2026-12", "meta_vendas": 600000},
]


def extract_metas():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUT_DIR / f"metas_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as arquivo:
        json.dump(METAS, arquivo, ensure_ascii=False, indent=2)

    print(f"Metas extraídas: {file_path}")

    return str(file_path)


if __name__ == "__main__":
    extract_metas()
