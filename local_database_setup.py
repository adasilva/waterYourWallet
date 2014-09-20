import pymongo

# connect to local server
conn = pymongo.Connection('localhost')

# create a database 
db =  conn.waterwallet

# create a collection in the database
plants = db.plants


# Span data from: 
# http://www.ces.ncsu.edu/depts/hort/consumer/quickref/vegetable/plantingguide.html
plants.insert({'Name':'beans','span':6,'water':None})
plants.insert({'Name':'broccoli','span':18,'water':None})
plants.insert({'Name':'cabbage','span':12,'water':None})
plants.insert({'Name':'corn','span':12,'water':None})
plants.insert({'Name':'cucumber','span':10,'water':None})
plants.insert({'Name':'eggplant','span':24,'water':None})
plants.insert({'Name':'okra','span':12,'water':None})
plants.insert({'Name':'peppers','span':18,'water':None})
plants.insert({'Name':'chili pepper','span':15,'water':None})
plants.insert({'Name':'pumpkin','span':48,'water':None})
plants.insert({'Name':'spinach','span':6,'water':None})
plants.insert({'Name':'swiss chard','span':6,'water':None})
plants.insert({'Name':'tomato','span':18,'water':None})
plants.insert({'Name':'zucchini','span':24,'water':None})
plants.insert({'Name':'watermelon','span':60,'water':None})
