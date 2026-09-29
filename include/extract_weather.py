import json
from datetime import datetime
from pathlib import Path

import requests


OUTPUT_DIR = Path("/tmp/projeto-2/extract/weather")

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=-29.68"
    "&longitude=-51.13"
    "&current=temperature_2m,relative_humidity_2m,"
    "precipitation,wind_speed_10m"
)


def extract_weather():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUT_DIR / f"weather_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as arquivo:
        json.dump(data, arquivo, ensure_ascii=False, indent=2)

    print(f"Weather extraído: {file_path}")

    return str(file_path)


if __name__ == "__main__":
    extract_weather()
