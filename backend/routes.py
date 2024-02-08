from . import app
import os
import json
import pymongo
from flask import jsonify, request, Response,  make_response, abort, url_for  # noqa; F401
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
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"})


@app.route("/count")
def count():
    """Return length of data"""
    count = db.songs.count_documents({})
    return jsonify({"count": count}), 200


# Define routes for the song service

@app.route("/song", methods=["GET"])
def songs():
    """Return all songs"""
    songs = list(db.songs.find({}))

    # Convert ObjectId to string for each document
    for song in songs:
        song['_id'] = str(song['_id'])

    return jsonify({"songs": songs}), 200



@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    """Get a song by its id"""
    song = db.songs.find_one({"id": id})
    
    if song:
        # Convert ObjectId to string
        song["_id"] = str(song["_id"])
        return jsonify({"songs": [song]}), 200
    else:
        abort(404, {"message": f"Song with id {id} not found"})




@app.route("/song", methods=["POST"])
def create_song():
    """Create a new song"""
    data = request.json
    song_id = data.get("id")
    
    # Check if the song id already exists
    existing_song = db.songs.find_one({"id": song_id})
    if existing_song:
        return jsonify({"Message": f"song with id {song_id} already present"}), 302
    
    # Insert the new song into the database
    result = db.songs.insert_one(data)
    
    if result.inserted_id:
        return Response(
            response=json.dumps({"inserted id": str(result.inserted_id)}),
            status=201,
            mimetype="application/json"
        )
    else:
        return jsonify({"message": "Failed to add song"}), 500
    


@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):
    """Update an existing song"""
    # get data from the json body
    song_in = request.json

    # check if the song exists
    song = db.songs.find_one({"id": id})

    # if song does not exist, return 404
    if song == None:
        return {"message": "song not found"}, 404

    updated_data = {"$set": song_in}

    result = db.songs.update_one({"id": id}, updated_data)

    # if the song is found and updated, return the updated song
    if result.modified_count == 0:
        return {"message": "song found, but nothing updated"}, 200
    else:
        return parse_json(db.songs.find_one({"id": id})), 201
    


@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    """Delete an existing song"""
    # Use id from URL
    # Delete the song from the database
    result = db.songs.delete_one({"id": id})

    # Check if the song was found and deleted
    if result.deleted_count == 0:
        # If not found, return 404 with a message
        return jsonify({"message": "song not found"}), 404
    else:
        # If deleted successfully, return 204 No Content
        return "", 204
    