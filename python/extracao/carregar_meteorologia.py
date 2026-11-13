
import json
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Localização do projeto
RAIZ = Path(__file__).resolve().parents[2]
load_dotenv(RAIZ / ".env")

PASTA_RAW = RAIZ / "dados" / "raw"

# Conexão PostgreSQL
url = URL.create(
    "postgresql+psycopg",
    username=__import__("os").getenv("DB_USER"),
    password=__import__("os").getenv("DB_PASSWORD") or None,
    host=__import__("os").getenv("DB_HOST"),
    port=int(__import__("os").getenv("DB_PORT")),
    database=__import__("os").getenv("DB_NAME"),
)

engine = create_engine(url)

registros = []

# Ler os nove arquivos JSON
for arquivo in sorted(PASTA_RAW.glob("meteorologia_*_2025.json")):
    print(f"Lendo: {arquivo.name}")

    bruto = json.loads(arquivo.read_text(encoding="utf-8"))
    hourly = bruto["resposta"]["hourly"]

    quantidade = len(hourly["time"])

    for i in range(quantidade):
        registros.append({
            "cod_usina": bruto["cod_usina"],
            "data_hora": hourly["time"][i],
            "temperatura_2m": hourly["temperature_2m"][i],
            "precipitacao": hourly["precipitation"][i],
            "velocidade_vento_10m": hourly["wind_speed_10m"][i],
            "radiacao_solar": hourly["shortwave_radiation"][i],
            "latitude": bruto["parametros"]["latitude"],
            "longitude": bruto["parametros"]["longitude"],
            "fonte": "Open-Meteo",
            "data_extracao": bruto["data_extracao"],
        })

print(f"\nRegistros preparados: {len(registros)}")

# Inserir os dados em uma transação
with engine.begin() as conexao:
    conexao.execute(
        text("DELETE FROM raw.meteorologia_horaria")
    )

    comando = text("""
        INSERT INTO raw.meteorologia_horaria (
            cod_usina, data_hora, temperatura_2m,
            precipitacao, velocidade_vento_10m,
            radiacao_solar, latitude, longitude,
            fonte, data_extracao
        ) VALUES (
            :cod_usina, :data_hora, :temperatura_2m,
            :precipitacao, :velocidade_vento_10m,
            :radiacao_solar, :latitude, :longitude,
            :fonte, :data_extracao
        )
    """)

    tamanho_lote = 1000

    for inicio in range(0, len(registros), tamanho_lote):
        lote = registros[inicio:inicio + tamanho_lote]
        conexao.execute(comando, lote)
        print(f"Inseridos: {min(inicio + tamanho_lote, len(registros))}")

print("\nCARGA CONCLUÍDA!")

# Conferir total no banco
with engine.connect() as conexao:
    total = conexao.execute(
        text("SELECT COUNT(*) FROM raw.meteorologia_horaria")
    ).scalar_one()

    print("Total de registros no PostgreSQL:", total)

engine.dispose()
