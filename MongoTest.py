from pymongo import MongoClient

client = MongoClient('34.74.70.39', 27017)  # подключение к машине
db = client.db
collections = db.list_collection_names()
print(collections)
# for i, collection in enumerate(collections):
#     if i == 0:
#         for n in collection.find({}):
#             print(n)
