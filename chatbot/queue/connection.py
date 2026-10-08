from redis import Redis
from rq import Queue

from chatbot.config import REDIS_QUEUE_NAME, REDIS_URL

_redis_conn: Redis | None = None
_queue: Queue | None = None


def get_redis() -> Redis:
    global _redis_conn
    if _redis_conn is None:
        _redis_conn = Redis.from_url(REDIS_URL)
    return _redis_conn


def get_queue() -> Queue:
    global _queue
    if _queue is None:
        _queue = Queue(REDIS_QUEUE_NAME, connection=get_redis())
    return _queue
