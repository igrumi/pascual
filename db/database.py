import asyncpg
import os

async def get_pool():
    db = os.getenv("PG_DB_NAME")
    user = os.getenv("PG_USER")
    pwd = os.getenv("PG_PASSWORD")
    host = os.getenv("PG_HOST")

    if not all([db, user, pwd, host]):
        raise ValueError("Missing one or more required environment variables: PG_DB_NAME, PG_USER, PG_PASSWORD, PG_HOST")

    return await asyncpg.create_pool(
        user=user,
        password=pwd,
        database=db,
        host=host
    )
