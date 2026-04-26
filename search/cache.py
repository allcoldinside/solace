_cache = {}

def get(k): return _cache.get(k)
def set(k, v): _cache[k] = v
