from redis import Redis
from datetime import datetime, timedelta
import numpy as np
from app.settings import settings

r = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)

ttl_secs = settings.HISTORY_TTL_DAYS * 24 * 3600


def _key(metric: str, part: str, day: str):
    return f"{metric}:{day}:{part}"


def store(metric: str, part: str, value: int, ts: datetime):
    k = _key(metric, part, ts.strftime("%Y-%m-%d"))
    r.hset(k, mapping={"value": value, "created_at": ts.isoformat()})
    r.expire(k, ttl_secs)


def window(metric: str, part: str, weeks: int = 8):
    vals = list()
    today = datetime.now().date()

    for w in range(1, weeks + 1):
        day = (today - timedelta(weeks=w)).strftime("%Y-%m-%d")
        v = r.hget(_key(metric, part, day), "value")
        vals.append(int(v) if v is not None else 0)

    return np.array(vals)
