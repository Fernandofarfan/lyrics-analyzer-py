from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
import sys  # Importa el módulo sys para utilizar sys.exit(1)

# Rutas al archivo JSON local
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")

# Cargar los datos desde el archivo JSON
with open(json_url) as f:
    songs_list = json.load(f)

# Configuración de conexión a MongoDB desde variables de entorno
mongodb_service = os.environ.get('MONGODB_SERVICE')
mongodb_username = os.environ.get('MONGODB_USERNAME')
mongodb_password = os.environ.get('MONGODB_PASSWORD')
mongodb_port = os.environ.get('MONGODB_PORT')

# Validar la existencia de la variable de servicio de MongoDB
if not mongodb_service:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)  # Utiliza sys.exit(1) para salir del programa con un código de error

# Construir la URL de conexión a MongoDB
if mongodb_username and mongodb_password:
    url = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}"
else:
    url = f"mongodb://{mongodb_service}"

# Intentar conectar con MongoDB
try:
    client = MongoClient(url)
    db = client.songs  # Seleccionar la base de datos "songs"
    db.songs.drop()  # Eliminar colección existente (opcional)
    db.songs.insert_many(songs_list)  # Insertar datos desde el archivo JSON en la colección "songs"
    print("Data successfully inserted into MongoDB.")
except OperationFailure as e:
    app.logger.error(f"Error connecting to MongoDB: {str(e)}")
    sys.exit(1)

def parse_json(data):
    return json.loads(json_util.dumps(data))


######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify(dict(status="healthy")), 200

######################################################################
# COUNT SONGS
######################################################################
@app.route("/count")
def count():
    """Returns the total number of songs."""
    count = db.songs.count_documents({})
    return jsonify(dict(count=count)), 200

######################################################################
# LIST SONGS
######################################################################
@app.route("/song", methods=["GET"])
def get_songs():
    """Returns a list of all songs."""
    songs = list(db.songs.find({}))
    return make_response(jsonify(parse_json(songs)), 200)

######################################################################
# GET A SONG BY ID
######################################################################
@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    """Returns a specific song by its ID."""
    song = db.songs.find_one({"id": id})
    if not song:
        return jsonify({"message": f"Song with id {id} not found"}), 404
    return make_response(jsonify(parse_json(song)), 200)

######################################################################
# CREATE A SONG
######################################################################
@app.route("/song", methods=["POST"])
def create_song():
    """Creates a new song."""
    new_song = request.get_json()
    
    # Check if song already exists
    song = db.songs.find_one({"id": new_song["id"]})
    if song:
        return jsonify({"Code": "CONN_CONFLICT", "Message": f"Song with id {new_song['id']} already exists"}), 409

    insert_id = db.songs.insert_one(new_song)
    return make_response(jsonify({"inserted id": str(insert_id.inserted_id)}), 201)

######################################################################
# UPDATE A SONG
######################################################################
@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):
    """Updates an existing song."""
    song_data = request.get_json()
    
    song = db.songs.find_one({"id": id})
    if not song:
        return jsonify({"message": "song not found"}), 404

    updated_song = db.songs.update_one({"id": id}, {"$set": song_data})
    
    if updated_song.modified_count == 0:
        return jsonify({"message": "song not updated"}), 200
    
    return make_response(jsonify(parse_json(db.songs.find_one({"id": id}))), 201)

######################################################################
# DELETE A SONG
######################################################################
@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    """Deletes a song by its ID."""
    result = db.songs.delete_one({"id": id})
    if result.deleted_count == 0:
        return jsonify({"message": "song not found"}), 404
        
    return "", 204
