import redis
import csv
from datetime import date
import json


r = redis.StrictRedis(host='localhost', port=6379, db=0)
allData = []
for key in r.keys():
    # print(key, r.get(key))
    data = json.loads(r.get(key))
    allData.append(data)

# print(allData)
# print()
today = date.today()
# dd/mm/YY
d1 = today.strftime("%d-%m-%Y")

with open('savedData/data'+str(d1)+".csv", mode='w',  encoding='utf16') as dataFile:
    dataFile = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    dataFile.writerow(['userId', 'chatId', 'username', 'studentID' , 'fullName', 'WantsChild' , 'parentHood' , 'lang'])

    for i in range(0, len(allData)):

        dictionary = allData[i]
        a = dictionary['userId']
        b = dictionary['chatId']
        c = dictionary['username']
        d = '-none-'
        e = '-none-'
        f = '-none-'
        g = '-none-'
        h = '-none-'

        if 'studentID' in dictionary:
            d = dictionary['studentID']

        if 'fullName' in dictionary:
            e = dictionary['fullName']
            
        if 'WantsChild' in dictionary:
            f = dictionary['WantsChild']
        
        if 'parentHood' in dictionary:
            g = dictionary['parentHood']
        
        if 'lang' in dictionary:
            h = dictionary['lang']
        print(a, b , c ,d , e , f, g, h)
        dataFile.writerow( [a, b , c ,d , e , f, g, h] )