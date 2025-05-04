import asyncio
import httpx
import psycopg
import os
from datetime import datetime, timezone

PG_DSN = os.getenv("PG_DSN")
SYMBOL = "bitcoin"
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

print('Hi')

async def fetch_price(client: httpx.AsyncClient) -> float:
    response = await client.get(
        COINGECKO_URL, params={"ids": SYMBOL, "vs_currencies": "usd"}
    )
    response.raise_for_status()
    print('response.json()', response.json())
    return response.json()[SYMBOL]["usd"]


async def insert_price(conn: psycopg.AsyncConnection, price: float):
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    async with conn.cursor() as cur:
        await cur.execute(
            """
            INSERT INTO crypto.candles (symbol, bucket_ts, open, high, low, close)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, bucket_ts) DO UPDATE
            SET high = GREATEST(crypto.candles.high, EXCLUDED.high),
                low  = LEAST(crypto.candles.low,  EXCLUDED.low),
                close= EXCLUDED.close
            """,
            (SYMBOL, now, price, price, price, price),
        )
    await conn.commit()


async def main():
    conn = await psycopg.AsyncConnection.connect(PG_DSN)
    print('Connection', conn.info)
    async with conn:
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    price = await fetch_price(client)
                    await insert_price(conn, price)
                except Exception as e:
                    print(f"[ERROR] {e}")
                await asyncio.sleep(60)


if __name__ == "__main__":
    print('teste')
    asyncio.run(main())
