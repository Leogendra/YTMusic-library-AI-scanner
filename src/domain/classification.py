from src.domain.soundproof_artist import SoundProofArtist
from src.domain.artist_name import normalize_artist_name
from src.domain.artist_status import ArtistStatus
from src.domain.track_verdict import TrackVerdict
from src.domain.track_artist import TrackArtist
from collections.abc import Iterable

MINIMUM_AI_VOTES = 1

# When a track has several artists, the most alarming verdict wins: one AI artist is enough to flag the track.
_STATUS_PRIORITY: tuple[ArtistStatus, ...] = (
    ArtistStatus.AI,
    ArtistStatus.TIE,
    ArtistStatus.HUMAN,
    ArtistStatus.UNKNOWN,
)




def classify_artist(entry: SoundProofArtist | None) -> ArtistStatus:
    """Classify an artist from its SoundProof votes.

    The precomputed "votes" field of the dump is ignored because it does not always equal ai_votes - human_votes.
    """
    if entry is None:
        return ArtistStatus.UNKNOWN
    elif entry.ai_votes > entry.human_votes:
        return ArtistStatus.AI
    elif entry.ai_votes < entry.human_votes:
        return ArtistStatus.HUMAN
    else:
        return ArtistStatus.TIE


def classify_track(artist_statuses: Iterable[ArtistStatus]) -> ArtistStatus:
    """Aggregate the verdicts of a track's artists into the verdict of the track."""
    present_statuses = set(artist_statuses)
    for status in _STATUS_PRIORITY:
        if status in present_statuses:
            return status
    return ArtistStatus.UNKNOWN


def is_flagged_artist(entry: SoundProofArtist | None, include_outvoted_artists: bool) -> bool:
    """Tell whether the artist must be reported.

    An artist needs at least one AI vote. Unless outvoted artists are included, the AI votes must also be at least as many as the human votes.
    """
    if entry is None or entry.ai_votes < MINIMUM_AI_VOTES:
        return False
    elif include_outvoted_artists:
        return True
    else:
        return entry.ai_votes >= entry.human_votes


def select_flagged_tracks(verdicts: Iterable[TrackVerdict], include_outvoted_artists: bool) -> list[TrackVerdict]:
    """Keep the tracks having at least one flagged artist, whatever the overall verdict."""
    return [
        verdict
        for verdict in verdicts
        if any(is_flagged_artist(match.entry, include_outvoted_artists) for match in verdict.artist_matches)
    ]


def select_unknown_artists(verdicts: Iterable[TrackVerdict]) -> list[TrackArtist]:
    """List once each artist of the tracks missing from the database, ignoring the artists featured on a known track.

    Artists are deduplicated by channel id, or by normalized name when they have no artist page.
    """
    unknown_artists: dict[str, TrackArtist] = {}
    for verdict in verdicts:
        if verdict.status is ArtistStatus.UNKNOWN:
            for match in verdict.artist_matches:
                unknown_artists.setdefault(_artist_key(match.artist), match.artist)
    return list(unknown_artists.values())


def _artist_key(artist: TrackArtist) -> str:
    if artist.channel_id is not None:
        return artist.channel_id
    else:
        return normalize_artist_name(artist.name)


def most_ai_voted_flagged_artist(verdict: TrackVerdict, include_outvoted_artists: bool) -> SoundProofArtist | None:
    """Return the flagged artist of the track with the most AI votes, or None when no artist is flagged.

    It is the single reference for the AI votes and the verification flag shown for a track, so both always describe the same artist.
    """
    flagged_entries = [
        match.entry
        for match in verdict.artist_matches
        if is_flagged_artist(match.entry, include_outvoted_artists)
    ]
    return max(flagged_entries, key=lambda entry: entry.ai_votes, default=None)
