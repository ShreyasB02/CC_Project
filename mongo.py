from pymongo import MongoClient

connectionstr="mongodb+srv://ccrmq:ccrmq@cluster0.s2ksf4g.mongodb.net/test"
client = MongoClient(connectionstr)

db = client['studentdb']
collection = db['student']
collection.insert_one({'srn':'pes1ug20cs395'})
print(collection)