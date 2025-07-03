import redis
import json
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

import time

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def save_to_memory(user_id: str, category: str, fact: str):
    key = f"user:{user_id}:memory:{category}"
    if not r.sismember(key, fact):  # Only store if it's not already there
        r.sadd(key, fact)
        print(f"Stored fact: '{fact}' in category '{category}' for user '{user_id}'")
        _in_memory_cache.pop(f"user:{user_id}:memory_cache", None)


def get_memory_by_category(user_id: str, category: str):
    key = f"user:{user_id}:memory:{category}"
    return list(r.smembers(key))



# Simple in-process memory cache
_in_memory_cache = {}

CACHE_TTL = 3600  # seconds (tune as needed)

def get_all_user_memory(user_id: str) -> list[str]:
    cache_key = f"user:{user_id}:memory_cache"
    now = time.time()

    # Check if in cache and not expired
    if cache_key in _in_memory_cache:
        cached_data, timestamp = _in_memory_cache[cache_key]
        if now - timestamp < CACHE_TTL:
            return cached_data

    # If not cached or expired, fetch from Redis
    keys = r.keys(f"user:{user_id}:memory:*")
    all_facts = []
    for key in keys:
        facts = r.smembers(key)
        category = key.split(":")[-1]
        all_facts.extend([f"[{category}] {fact}" for fact in facts])

    # Update cache
    _in_memory_cache[cache_key] = (all_facts, now)
    return all_facts

