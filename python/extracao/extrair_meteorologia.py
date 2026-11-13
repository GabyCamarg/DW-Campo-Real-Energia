
import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential


# Caminhos do projeto
RAIZ = Path(__file__).resolve().parents[2]
load_dotenv(RAIZ / ".env")

ARQUIVO_USINAS = RAIZ / "config" / "usinas_referencia.csv"
PASTA_RAW = RAIZ / "dados" / "raw"
PASTA_LOGS = RAIZ / "dados" / "logs"

PASTA_RAW.mkdir(parents=True, exist_ok=True)
PASTA_LOGS.mkdir(parents=True, exist_ok=True)

ARQUIVO_LOG = PASTA_LOGS / "extracao_meteorologia_2025.csv"

# API Open-Meteo
URL = "https://archive-api.open-meteo.com/v1/archive"

VARIAVEIS = [
    "temperature_2m",
    "precipitation",
    "wind_speed_10m",
    "shortwave_radiation",
]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=10),
    reraise=True,
)
def consultar_api(parametros):
    resposta = requests.get(
        URL,
        params=parametros,
        timeout=60,
    )
    resposta.raise_for_status()
    return resposta.json()


def registrar_log(registro):
    existe = ARQUIVO_LOG.exists()

    with open(ARQUIVO_LOG, "a", newline="", encoding="utf-8") as arquivo:
        campos = [
            "cod_usina",
            "inicio",
            "fim",
            "status",
            "registros",
            "arquivo",
            "erro",
        ]

        escritor = csv.DictWriter(arquivo, fieldnames=campos)

        if not existe:
            escritor.writeheader()

        escritor.writerow(registro)


def extrair_usina(usina):
    inicio = datetime.now().astimezone().isoformat()
    codigo = usina["cod_usina"]

    logging.info("Iniciando extração: %s", codigo)

    parametros = {
        "latitude": float(usina["latitude"]),
        "longitude": float(usina["longitude"]),
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "hourly": VARIAVEIS,
        "timezone": "America/Sao_Paulo",
    }

    try:
        dados = consultar_api(parametros)

        horario = dados.get("hourly", {}).get("time", [])

        if not horario:
            raise ValueError("A API retornou dados horários vazios.")

        for variavel in VARIAVEIS:
            valores = dados["hourly"].get(variavel)

            if valores is None or len(valores) != len(horario):
                raise ValueError(
                    f"Dados ausentes ou inconsistentes: {variavel}"
                )

        nome_arquivo = f"meteorologia_{codigo}_2025.json"
        caminho = PASTA_RAW / nome_arquivo

        registro_bruto = {
            "fonte": "Open-Meteo Historical Weather API",
            "url": URL,
            "parametros": parametros,
            "cod_usina": codigo,
            "nome_usina": usina["nome"],
            "data_extracao": datetime.now().astimezone().isoformat(),
            "resposta": dados,
        }

        caminho.write_text(
            json.dumps(registro_bruto, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        fim = datetime.now().astimezone().isoformat()

        registrar_log({
            "cod_usina": codigo,
            "inicio": inicio,
            "fim": fim,
            "status": "SUCESSO",
            "registros": len(horario),
            "arquivo": str(caminho.relative_to(RAIZ)),
            "erro": "",
        })

        logging.info(
            "Concluído: %s - %s registros",
            codigo,
            len(horario),
        )

        return True

    except Exception as erro:
        fim = datetime.now().astimezone().isoformat()

        registrar_log({
            "cod_usina": codigo,
            "inicio": inicio,
            "fim": fim,
            "status": "ERRO",
            "registros": 0,
            "arquivo": "",
            "erro": str(erro),
        })

        logging.exception("Falha na extração de %s", codigo)
        return False


def main():
    usinas = pd.read_csv(ARQUIVO_USINAS)

    if len(usinas) != 9:
        raise ValueError(
            f"Esperadas 9 usinas, mas foram encontradas {len(usinas)}."
        )

    sucessos = 0
    falhas = 0

    for _, usina in usinas.iterrows():
        if extrair_usina(usina):
            sucessos += 1
        else:
            falhas += 1

        time.sleep(1)

    print("\n========== RESULTADO DA EXTRAÇÃO ==========")
    print("Usinas processadas:", len(usinas))
    print("Extrações concluídas:", sucessos)
    print("Extrações com erro:", falhas)
    print("Pasta dos dados brutos:", PASTA_RAW)
    print("Arquivo de log:", ARQUIVO_LOG)

    if falhas:
        print("\nATENÇÃO: verifique as falhas no arquivo de log.")
    else:
        print("\nEXTRAÇÃO CONCLUÍDA COM SUCESSO!")


if __name__ == "__main__":
    main()
