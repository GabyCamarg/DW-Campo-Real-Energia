import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

url = URL.create(
    "postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD") or None,
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(url)

consulta = """
SELECT
    cod_usina,
    nome,
    municipio,
    uf,
    latitude,
    longitude,
    potencia_mw
FROM campo_real_energia.usina
WHERE cod_usina <> 'CRE-ERR-010'
ORDER BY cod_usina;
"""

with engine.connect() as conexao:
    df = pd.read_sql(text(consulta), conexao)

print("USINAS ENCONTRADAS:", len(df))
print(df.to_string(index=False))
