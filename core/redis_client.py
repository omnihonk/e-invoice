import redis
import json
from typing import Optional
from schemas.session import InvoiceSession
import os

# Use a default fallback for local dev
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

_in_memory_db = {}

use_redis = False
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1)
    redis_client.ping()
    use_redis = True
except Exception:
    # Fail silently and fall back to in-memory dict
    pass

def get_session(session_id: str) -> Optional[InvoiceSession]:
    if use_redis:
        try:
            data = redis_client.get(f"session:{session_id}")
            if data:
                return InvoiceSession.model_validate_json(data)
        except Exception:
            pass
    
    # Fallback to in-memory store
    data = _in_memory_db.get(f"session:{session_id}")
    if data:
        return InvoiceSession.model_validate_json(data)
    return None

def save_session(session: InvoiceSession, ttl_seconds: int = 3600):
    if use_redis:
        try:
            redis_client.setex(
                f"session:{session.session_id}",
                ttl_seconds,
                session.model_dump_json()
            )
            return
        except Exception:
            pass
            
    # Fallback to in-memory store
    _in_memory_db[f"session:{session.session_id}"] = session.model_dump_json()
