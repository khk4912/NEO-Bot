import asyncio

import aiomysql

from CONFIG import DB_NAME, DB_PW, DB_USER


class DBHandler:
    def __init__(self, loop=None) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.conn_pool = None

    async def make_pool(self) -> None:
        self.conn_pool = await aiomysql.create_pool(
            host="localhost",
            user=DB_USER,
            password=DB_PW,
            db=DB_NAME,
            autocommit=True,
            loop=self.loop,
            minsize=2,
            maxsize=10,
            charset="utf8mb4",
        )

    async def execute(self, query: str, args: tuple = None):
        assert self.conn_pool is not None
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
        return cur
