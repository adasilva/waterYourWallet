import pymongo

# connect to local server
conn = pymongo.Connection('localhost')

# create a database 
db =  conn.gardendb

# create a collection in the database
plants = db.plants

# add plants to the collection
# Note: I'm not sure if the properties are correct! For example only :)
plants.insert({'Name':'tomato','size':'Large','water':1})
plants.insert({'Name':'pepper','size':'Medium','water':1})
plants.insert({'Name':'lemon verbena','size':'Large','water':.25})
plants.insert({'Name':'basil','size':'Medium','water':1})
plants.insert({'Name':'thyme','size':'small','water':.5})

