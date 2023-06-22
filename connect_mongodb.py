#!/usr/bin/python
import pymongo

from config import config_mongodb

# Replace the uri string with your MongoDB deployment's connection string.
params = config_mongodb()
CONN_STR = (
    "mongodb://"
    + f"{params['username']}:{params['password']}"
    + f"@{params['host']}:{params['port']}"
    + "/?authMechanism=DEFAULT"
)
# set a 5-second connection timeout
client = pymongo.MongoClient(CONN_STR, serverSelectionTimeoutMS=5000)
try:
    print(client.list_database_names())
except Exception as error:
    print("Unable to connect to the server.\n", error)
