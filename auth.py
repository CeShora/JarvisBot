import redis
import json

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def isAuth(username):
    colledctedData = r.get('StudentId_Username_CollectedData')
    colledctedDataDictionary = json.loads(r.get(colledctedData))
    if not colledctedDataDictionary[username] == None :
        return True
