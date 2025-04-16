# init_db.py
import os
import asyncio
import asyncpg
from dotenv import load_dotenv

load_dotenv()

PG_DB_NAME = os.getenv("PG_DB_NAME", "pascualbot")
PG_USER = os.getenv("PG_USER", "pascualillo")
PG_PASSWORD = os.getenv("PG_PASSWORD", "pascualtoiletsigma119")
PG_HOST = os.getenv("PG_HOST", "db")
PG_PORT = os.getenv("PG_PORT", "5432")


async def create_database_if_not_exists():
    conn = await asyncpg.connect(
        user=PG_USER,
        password=PG_PASSWORD,
        database="postgres",  # Conectamos a la base "postgres" para poder crear otra
        host=PG_HOST,
        port=PG_PORT,
    )

    # Verifica si la base ya existe
    db_exists = await conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname = $1", PG_DB_NAME
    )
    if not db_exists:
        print(f"[~] Creando base de datos: {PG_DB_NAME}")
        await conn.execute(f'CREATE DATABASE "{PG_DB_NAME}";')
    else:
        print(f"[✓] La base de datos {PG_DB_NAME} ya existe.")

    await conn.close()


async def init_database():
    await create_database_if_not_exists()

    # Conectamos a la base que queremos inicializar
    conn = await asyncpg.connect(
        user=PG_USER,
        password=PG_PASSWORD,
        database=PG_DB_NAME,
        host=PG_HOST,
        port=PG_PORT,
    )

    print("[+] Conectado a la base:", PG_DB_NAME)
    with open("db/schema.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    await conn.execute(sql_script)
    await conn.close()
    print("[✓] Base de datos inicializada correctamente")


if __name__ == "__main__":
    asyncio.run(init_database())
