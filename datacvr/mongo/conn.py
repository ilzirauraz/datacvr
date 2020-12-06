from pymongo import MongoClient


def open_connection():
    uri = "" # your URI, ex.: "mongodb+srv://<user>:<pass>@<host>/<db>?retryWrites=true&w=majority"
    return MongoClient(uri)
