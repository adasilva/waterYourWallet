import pymongo
import re  #regular expressions for matching strings


conn = pymongo.Connection('localhost')
db =  conn.gardendb
plants = db.plants

def find_by_name(string):
    '''Finds a plant by name'''
    regx = re.compile('^'+string, re.IGNORECASE)
    retList = []
    for p in plants.find({'Name':regx}):
        retList.append(p['Name'])

    return retList
