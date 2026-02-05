from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

SETTINGS_FILE = "/config/Settings.json"

# Static album lookup: display name -> album UUID
# Update these with your actual Immich album names and IDs
ALBUMS = {
    "Family Photos": "fa5b1c3d-942a-46fb-9f6e-6e8edc3507e0",
    "Photography Collection": "02f05303-62cc-4c31-a4c6-b17f3096b1c2",
    "Nabayi Collection": "f22a99a8-cc52-490a-aa52-28781f7dbb8b",
    "Rimna Collection": "d8d7bdb5-e105-4fda-bad7-7804e32ea971",
    "Bruki Collection": "625f2b8c-8b2f-4dad-91d5-6a9fec7e7159",
    "Generic Album 1": "8bbad008-0341-4031-8786-698ac2575166",
    "Generic Album 2": "42c3071a-b828-46cd-8e96-940934fbeef9",
}

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

@app.route("/")
def index():
    settings = load_settings()
    current_album_ids = settings.get("Accounts", [{}])[0].get("Albums", [])
    return render_template("index.html", settings=settings, albums=ALBUMS, current_album_ids=current_album_ids)

@app.route("/api/settings", methods=["GET"])
def get_settings():
    return jsonify(load_settings())

@app.route("/api/settings", methods=["POST"])
def update_settings():
    try:
        new_settings = request.json
        save_settings(new_settings)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/albums/add", methods=["POST"])
def add_album():
    try:
        album_id = request.json.get("album_id")
        if not album_id:
            return jsonify({"status": "error", "message": "No album_id provided"}), 400
        settings = load_settings()
        albums = settings["Accounts"][0].get("Albums", [])
        if album_id in albums:
            return jsonify({"status": "error", "message": "Album already added"}), 400
        albums.append(album_id)
        settings["Accounts"][0]["Albums"] = albums
        save_settings(settings)
        return jsonify({"status": "success", "albums": albums})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/albums/remove", methods=["POST"])
def remove_album():
    try:
        album_id = request.json.get("album_id")
        if not album_id:
            return jsonify({"status": "error", "message": "No album_id provided"}), 400
        settings = load_settings()
        albums = settings["Accounts"][0].get("Albums", [])
        if album_id not in albums:
            return jsonify({"status": "error", "message": "Album not found"}), 400
        albums.remove(album_id)
        settings["Accounts"][0]["Albums"] = albums
        save_settings(settings)
        return jsonify({"status": "success", "albums": albums})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
