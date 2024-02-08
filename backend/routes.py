from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys


# Define MongoDB connection details
mongodb_service = 'localhost'
mongodb_username = None
mongodb_password = None
mongodb_port = 27017  # Default MongoDB port

# Construct MongoDB connection URL
if mongodb_username and mongodb_password:
    connection_url = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}:{mongodb_port}/"
else:
    connection_url = f"mongodb://{mongodb_service}:{mongodb_port}/"

# Connect to MongoDB
try:
    client = MongoClient(connection_url)
except pymongo.errors.OperationFailure as e:
    print(f"MongoDB connection failed: {e}")
    sys.exit(1)

# Define other variables and operations as needed
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))

db = client.songs
db.songs.drop()
db.songs.insert_many(songs_list)

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# INSERT CODE HERE
######################################################################
