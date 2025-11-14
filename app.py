import json
from flask import Flask, Response, request
from youtube_api import YoutubeAPI

app = Flask(__name__)
youtube_api = YoutubeAPI()


@app.route("/")
def home():
    return Response("Welcome to Youtube API", headers={"live": True})


# === ROUTE 1: SEARCH SONG ===
@app.route("/search-song", methods=["GET"])
def search_song():
    query = request.args.get("query")
    try:
        limit = min(int(request.args.get("limit")), 3)
    except:
        limit = 3

    if not query:
        return "Missing query parameter"

    try:
        result = youtube_api.search_video(query, limit)
        return json.dumps(result)
    except:
        return "Failed to fetch query"


# === ROUTE 2: DOWNLOAD SONG ===
@app.route("/download-song", methods=["GET"])
def download_song():
    link = request.args.get("link")

    if not link:
        return Response(b"", mimetype="application/octet-stream")

    try:
        audio_bytes = youtube_api.get_audio_buffer(link)
        return Response(audio_bytes, mimetype="audio/webm")
    except:
        return Response(b"", mimetype="application/octet-stream")
