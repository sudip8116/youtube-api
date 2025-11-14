from io import BytesIO
from youtubesearchpython import VideosSearch
from pytubefix import YouTube


class YoutubeAPI:
    def __init__(self):
        self.max_video_length = 10  # minute
        
    def search_video(self, query: str, limit: int):
        videos = VideosSearch(query, limit=5).result()

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
                _min = int(parts[0])
                if _min <= self.max_video_length:
                    return True
            except:
                return False
        return False

    def download_audio(self, link: str):
        youtube = YouTube(link)
        audio = youtube.streams.filter(only_audio=True).order_by("abr").desc().first()

        buffer = BytesIO()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)

        return buffer.read()
