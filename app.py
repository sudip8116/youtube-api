import json
from flask import Flask, Response, request, jsonify
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
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    return json.dumps(youtube_api.search_video(query, limit))


# === ROUTE 2: DOWNLOAD SONG ===
@app.route("/download-song", methods=["GET"])
def download_song():
    link = request.args.get("link")
    if not link:
        return Response(b"", mimetype="application/octet-stream")
    try:
        buffer = youtube_api.get_audio_buffer(link)
        return Response(buffer, mimetype="application/octet-stream")
    except:
        return Response(b"", mimetype="application/octet-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
