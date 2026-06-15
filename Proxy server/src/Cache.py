
import time
from collections import OrderedDict
from Config import CACHE_CAPACITY, CACHE_TTL_SECONDS

class CacheEntry:
    def __init__(self, response_bytes, timestamp=None, headers=None):
        self.data = response_bytes
        self.time = timestamp if timestamp is not None else time.time()
        self.headers = headers or {}


class LRUCache:
    def __init__(self, capacity=CACHE_CAPACITY, ttl=CACHE_TTL_SECONDS):
        self.capacity = capacity
        self.ttl = ttl
        self.store = OrderedDict() 


    def _is_expired(self, entry: CacheEntry) -> bool:
        return (time.time() - entry.time) > self.ttl
    

    def get(self, key: str):
        entry = self.store.get(key)
        if not entry:
            return None
        if self._is_expired(entry):
            try:
                del self.store[key]
            except KeyError:
                pass
            return None
        try:
            self.store.move_to_end(key, last=True)
        except Exception:
            pass
        return entry.data


    def save(self, key: str, response_bytes: bytes, headers: dict = None):
        if key in self.store:
            try:
                del self.store[key]
            except KeyError:
                pass
        while len(self.store) >= self.capacity:
            try:
                self.store.popitem(last=False)
            except Exception:
                break
        self.store[key] = CacheEntry(response_bytes, time.time(), headers)


    def info(self):
        return [(k, v.time) for k, v in self.store.items()]


cache = LRUCache()
