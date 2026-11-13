import os
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

try:
    engine = create_engine(url)

    with engine.connect() as conexao:
        resultado = conexao.execute(text("SELECT version();"))
        print("CONEXÃO REALIZADA COM SUCESSO!")
        print(resultado.scalar())

except Exception as erro:
    print("ERRO AO CONECTAR AO POSTGRESQL:")
    print(erro)
