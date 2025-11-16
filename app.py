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
        limit = min(int(request.args.get("limit")), 5)
    except:
        limit = 5

    if not query:
        return json.dumps({"error": True})

    try:
        result = youtube_api.search_video(query, limit)
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": True})


# === ROUTE 2: DOWNLOAD SONG ===
@app.route("/get-audio-url")
def download_song():
    link = request.args.get("link")
    if not link:
        return "error"

    try:
        url = youtube_api.get_audio_url(link)
        return url
    except Exception as e:
        return "error"


if __name__ == "__main__":
    app.run("0.0.0.0")
