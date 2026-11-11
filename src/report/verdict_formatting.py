from src.domain.track_verdict import TrackVerdict

YOUTUBE_MUSIC_WATCH_URL = "https://music.youtube.com/watch?v="




def track_url(verdict: TrackVerdict) -> str | None:
    if verdict.track.video_id is None:
        return None
    else:
        return YOUTUBE_MUSIC_WATCH_URL + verdict.track.video_id
