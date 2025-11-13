from flask import Flask, request, jsonify, send_file
from youtubesearchpython import VideosSearch
from pytubefix import YouTube
import os

app = Flask(__name__)

# === ROUTE 1: SEARCH SONG ===
@app.route('/search-song', methods=['GET'])
def search_song():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    videos = VideosSearch(query, limit=5).result()
    results = []

    for video in videos.get("result", []):
        results.append({
            "title": video.get("title"),
            "duration": video.get("duration"),
            "url": video.get("link"),
            "thumbnail": video.get("thumbnails", [{}])[0].get("url")
        })

    return jsonify(results)


# === ROUTE 2: DOWNLOAD SONG ===
@app.route('/download-song', methods=['GET'])
def download_song():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing query parameter 'url'"}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        if not stream:
            return jsonify({"error": "No audio stream found"}), 404

        out_file = stream.download(filename="song.mp4")
        new_file = "song.mp3"
        os.rename(out_file, new_file)

        return send_file(new_file, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up old files
        if os.path.exists("song.mp3"):
            os.remove("song.mp3")
        if os.path.exists("song.mp4"):
            os.remove("song.mp4")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

