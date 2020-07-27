import requests
from pymongo import MongoClient

# Client connects to "localhost" by default
client = MongoClient()
# Create local "nobel" database on the fly
db = client["nobel"]

# API documented at https://nobelprize.readme.io/docs/prize
for collection_name in ["prizes", "laureates"]:
    singular = collection_name[:-1]
    response = requests.get("http://api.nobelprize.org/v1/{}.json".format(singular))
    documents = response.json()[collection_name]
    # Access collections on the fly!
    db[collection_name].drop()  # Drop collection first if already exists
    db[collection_name].insert_many(documents)

# Check to make sure everything is correct
assert client.nobel == client["nobel"]
assert client.nobel.prizes == client["nobel"]["prizes"]
print(db.prizes.count_documents({}), "prize documents")
print(db.laureates.count_documents({}), "laureates documents")
