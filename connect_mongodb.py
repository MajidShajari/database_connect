#!/usr/bin/python
import pymongo

from config import config_mongodb
from custom_decorator import timeit


@timeit
def connect():
    # Replace the uri string with your MongoDB deployment's connection string.
    params = config_mongodb()
    conn_str = (
        "mongodb://"
        + f"{params['username']}:{params['password']}"
        + f"@{params['host']}:{params['port']}"
        + "/?authMechanism=DEFAULT"
    )
    # set a 5-second connection timeout
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        print(client.list_database_names())
    except Exception as error:
        print("Unable to connect to the server.\n", error)


if __name__ == "__main__":
    connect()
