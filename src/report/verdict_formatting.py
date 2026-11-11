from src.domain.track_verdict import TrackVerdict
from src.domain.artist_match import ArtistMatch

YOUTUBE_MUSIC_WATCH_URL = "https://music.youtube.com/watch?v="




def describe_artist_match(match: ArtistMatch) -> str:
    """Describe an artist with its SoundProof votes, e.g. "Cyndr (verified, 1000 AI / 0 human)"."""
    if match.entry is None:
        return f"{match.artist_name} (not in SoundProof)"
    else:
        verification = "verified" if match.entry.verified else "unverified"
        return f"{match.artist_name} ({verification}, {match.entry.ai_votes} AI / {match.entry.human_votes} human)"


def decisive_artist_matches(verdict: TrackVerdict) -> tuple[ArtistMatch, ...]:
    """Return the artists responsible for the track verdict, i.e. those sharing its status."""
    return tuple(match for match in verdict.artist_matches if match.status is verdict.status)


def track_url(verdict: TrackVerdict) -> str | None:
    if verdict.track.video_id is None:
        return None
    else:
        return YOUTUBE_MUSIC_WATCH_URL + verdict.track.video_id
