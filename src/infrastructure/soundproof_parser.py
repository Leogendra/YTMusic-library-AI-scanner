from src.domain.soundproof_artist import SoundProofArtist
import logging

_LOGGER = logging.getLogger(__name__)




class SoundProofFormatError(ValueError):
    """Raised when the SoundProof dump does not have the expected overall shape."""


def parse_soundproof_artists(raw_dump: object) -> list[SoundProofArtist]:
    """Convert the decoded JSON dump into typed entries.

    Malformed rows are skipped with a warning instead of aborting, because one bad community entry must not prevent analyzing the whole library.
    """
    if not isinstance(raw_dump, list):
        raise SoundProofFormatError(f"Expected a JSON list of artists, got {type(raw_dump).__name__}.")
    artists: list[SoundProofArtist] = []
    skipped_row_count = 0
    for row in raw_dump:
        artist = _parse_row(row)
        if artist is None:
            skipped_row_count += 1
        else:
            artists.append(artist)
    if skipped_row_count > 0:
        _LOGGER.warning("Skipped %d malformed SoundProof rows.", skipped_row_count)
    return artists


def _parse_row(row: object) -> SoundProofArtist | None:
    if not isinstance(row, dict):
        return None
    identifier = row.get("id")
    name = row.get("name")
    verified = row.get("verified")
    ai_votes = row.get("ai_votes")
    human_votes = row.get("human_votes")
    is_valid = (
        isinstance(identifier, str)
        and isinstance(name, str)
        and isinstance(verified, bool)
        and _is_vote_count(ai_votes)
        and _is_vote_count(human_votes)
    )
    if is_valid:
        return SoundProofArtist(
            identifier=identifier,
            name=name,
            verified=verified,
            ai_votes=ai_votes,
            human_votes=human_votes,
        )
    else:
        return None


def _is_vote_count(value: object) -> bool:
    # bool is a subclass of int in Python, so it must be excluded explicitly.
    return isinstance(value, int) and not isinstance(value, bool)
