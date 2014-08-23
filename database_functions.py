import pymongo
import re  #regular expressions for matching strings


conn = pymongo.Connection('localhost')
db =  conn.gardendb
plants = db.plants

def match_by_name(string):
    '''Finds a plant by name.

    Returns all plant names starting with the input string, ignoring capitalization.'''
    regx = re.compile('^'+string, re.IGNORECASE)
    retList = []
    for p in plants.find({'Name':regx}):
        retList.append(p['Name'])

    return retList

def get_properties_by_name(string):
    '''Returns properties of a plant by name. Right now this is a dummy function, it does not do anything!'''
    properties = {}
    return properties
