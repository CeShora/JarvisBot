import redis
import csv
from datetime import date
import json
import csv

with open('copy bot data - Sheet2.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    dataCollected = []
    a ={ }
    for row in csv_reader:
        a ={ }
        print(f'\t{row[0]} is the student id of person with username: {row[1]}')
        a [str(row[0])]= str(row[1])
        line_count += 1
        dataCollected.append(a)
    # print(dataCollected)
    print()
    print(len(dataCollected))
    print()

    print(f'Processed {line_count} lines.')
    #now we should save that data in a json file
    jsonDump = json.dumps(dataCollected)
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set("StudentId_Username_CollectedData", jsonDump)
    
# r = redis.Redis(host='localhost', port=6379, db=0)
# print(r.get("StudentId_Username_CollectedData"))
