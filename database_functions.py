import pymongo
import re  #regular expressions for matching strings

# Use local database:
#conn = pymongo.Connection('localhost')
#db =  conn.gardendb
#plants = db.plants

class plantdb:
    def __init__(self):
        '''The plantdb class contains functions for connecting to ObjectRocket remote database'''

        # Get password from configuration file
        with open('config.conf','r') as f:
            user = f.next().strip()
            passwd = f.next().strip()
            db_uri = 'mongodb://%s:%s@dfw-c9-1.objectrocket.com:37013/waterwallet' %(user,passwd)

        # Connect to database
        self.conn = pymongo.MongoClient(db_uri,slaveOK=True)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.conn.close()

    def match_by_name(self, string):
        '''Finds a plant by name.

        Returns all plant names starting with the input string, ignoring capitalization.'''
        print string
        regx = re.compile('^'+string, re.IGNORECASE)
        retList = []
        db = self.conn.waterwallet  # waterwallet database 
        plants = db.plants  # plants collection in waterwallet database
        for p in plants.find({'Name':regx}):
            retList.append(p['Name']) # for each match, append to return list
            if len(retList)>=4:
                break
        return retList

    def get_properties_by_name(self, string):
        '''Returns properties of a plant by name. Right now this is a dummy function, it does not do anything!'''
        db = self.conn.waterwallet  # waterwallet database 
        plants = db.plants  # plants collection in waterwallet database
        properties = plants.find_one({'Name':string})

        return properties
