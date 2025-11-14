from io import BytesIO
from youtubesearchpython import VideosSearch
from pytubefix import YouTube


class YoutubeAPI:
    def __init__(self):
        self.max_video_length = 10  # minutes

    def search_video(self, query: str, limit: int):
        videos = VideosSearch(query, limit=limit).result()

        results = []

        for video in videos.get("result", []):
            duration = video["duration"]
            if not self.fetch_duration(duration):
                continue

            results.append(video)
            if len(results) >= limit:
                break

        return results

    def fetch_duration(self, duration: str):
        parts = duration.split(":")
        if len(parts) == 2:
            try:
                minutes = int(parts[0])
                return minutes <= self.max_video_length
            except:
                return False
        return False

    def get_audio_url(self, link):
        yt = YouTube(link)
        audio = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
        return audio.url  # direct GoogleVideo URL
