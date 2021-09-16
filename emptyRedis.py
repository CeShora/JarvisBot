import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
for key in r.keys():
    print(key, r.get(key))
    r.delete(key)