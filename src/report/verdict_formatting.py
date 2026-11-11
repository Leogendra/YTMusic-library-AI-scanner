from src.domain.track_verdict import TrackVerdict
from urllib.parse import parse_qs, urlparse

YOUTUBE_MUSIC_WATCH_URL = "https://music.youtube.com/watch?v="




def track_url(verdict: TrackVerdict) -> str | None:
    if verdict.track.video_id is None:
        return None
    else:
        return YOUTUBE_MUSIC_WATCH_URL + verdict.track.video_id


def video_id_from_url(url: str) -> str | None:
    video_ids = parse_qs(urlparse(url).query).get("v")
    if video_ids:
        return video_ids[0]
    else:
        return None
