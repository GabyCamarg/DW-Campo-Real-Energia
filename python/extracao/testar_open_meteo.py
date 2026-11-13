import json
from datetime import datetime
from pathlib import Path

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

URL = "https://archive-api.open-meteo.com/v1/archive"

PARAMETROS = {
    "latitude": -15.803,
    "longitude": -43.308,
    "start_date": "2025-01-01",
    "end_date": "2025-01-03",
    "hourly": [
        "temperature_2m",
        "precipitation",
        "wind_speed_10m",
        "shortwave_radiation"
    ],
    "timezone": "America/Sao_Paulo"
}

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def consultar_api():
    resposta = requests.get(URL, params=PARAMETROS, timeout=60)
    resposta.raise_for_status()
    return resposta.json()

try:
    dados = consultar_api()

    if not dados.get("hourly", {}).get("time"):
        raise ValueError("A API retornou uma resposta sem dados horários.")

    pasta = Path("dados/raw")
    pasta.mkdir(parents=True, exist_ok=True)

    arquivo = pasta / "teste_open_meteo_ufv_janaina_2025.json"

    registro = {
        "fonte": "Open-Meteo Historical Weather API",
        "url": URL,
        "parametros": PARAMETROS,
        "data_extracao": datetime.now().astimezone().isoformat(),
        "resposta": dados
    }

    arquivo.write_text(
        json.dumps(registro, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("EXTRAÇÃO REALIZADA COM SUCESSO!")
    print("Usina: UFV Campo Real Minas")
    print("Município: Janaúba - MG")
    print("Quantidade de registros:", len(dados["hourly"]["time"]))
    print("Variáveis:", list(dados["hourly"].keys()))
    print("Arquivo bruto:", arquivo)

except Exception as erro:
    print("ERRO NA EXTRAÇÃO:", erro)
