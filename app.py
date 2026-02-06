from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

SETTINGS_FILE = "/config/Settings.json"
ALBUMS_FILE = "/config/albums.json"

def load_albums():
    if os.path.exists(ALBUMS_FILE):
        with open(ALBUMS_FILE, "r") as f:
            return json.load(f)
    return {}

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
    return render_template("index.html", settings=settings, albums=load_albums(), current_album_ids=current_album_ids)

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
