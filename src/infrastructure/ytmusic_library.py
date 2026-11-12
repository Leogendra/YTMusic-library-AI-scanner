from src.domain.removal_report import RemovalReport
from src.domain.library_track import LibraryTrack
from src.domain.track_artist import TrackArtist
from ytmusicapi.exceptions import YTMusicError
from typing import Any, Protocol
import logging
import json

_LOGGER = logging.getLogger(__name__)




class LibraryClient(Protocol):
    """The subset of the ytmusicapi client this adapter relies on."""

    def get_library_songs(self, limit: int | None = 25) -> list[dict[str, Any]]: ...

    def edit_song_library_status(self, feedbackTokens: list[str] | None = None) -> dict[str, Any]: ...


class YTMusicLibrary:
    """Library source and editor of the songs saved in a YouTube Music account."""

    def __init__(self, client: LibraryClient) -> None:
        self._client = client

    def fetch_tracks(self) -> list[LibraryTrack]:
        # A None limit makes ytmusicapi follow every continuation page instead of stopping at the first 25 songs.
        raw_songs = self._request_songs()
        tracks: list[LibraryTrack] = []
        for raw_song in raw_songs:
            track = _parse_song(raw_song)
            if track is None:
                _LOGGER.warning("Skipped a library song without title: %r", raw_song)
            else:
                tracks.append(track)
        return tracks

    def remove_tracks(self, video_ids: list[str]) -> RemovalReport:
        removal_tokens = self._find_removal_tokens(video_ids)
        # Tracks missing from the library, or without removal token, cannot be removed and are reported back.
        removable_video_ids = [video_id for video_id in video_ids if video_id in removal_tokens]
        processed_video_ids = self._send_removals(removable_video_ids, removal_tokens)
        not_removed_video_ids = tuple(video_id for video_id in video_ids if video_id not in processed_video_ids)
        return RemovalReport(removed_video_ids=tuple(processed_video_ids), not_removed_video_ids=not_removed_video_ids)

    def _find_removal_tokens(self, video_ids: list[str]) -> dict[str, str]:
        removal_tokens: dict[str, str] = {}
        for raw_song in self._request_songs():
            video_id = raw_song.get("videoId")
            removal_token = _parse_removal_token(raw_song)
            if video_id in video_ids and removal_token is not None:
                removal_tokens[video_id] = removal_token
        return removal_tokens

    def _send_removals(self, video_ids: list[str], removal_tokens: dict[str, str]) -> list[str]:
        if not video_ids:
            return []
        else:
            response = self._client.edit_song_library_status([removal_tokens[video_id] for video_id in video_ids])
            feedback_responses = response.get("feedbackResponses", [])
            return [
                video_id
                for video_id, feedback_response in zip(video_ids, feedback_responses)
                if feedback_response.get("isProcessed") is True
            ]

    def _request_songs(self) -> list[dict[str, Any]]:
        try:
            return self._client.get_library_songs(limit=None)
        except json.JSONDecodeError as error:
            # YouTube answers with an HTML error page when the headers are rejected, which ytmusicapi cannot decode.
            raise YTMusicError(
                "YouTube Music rejected the request (non-JSON answer). "
                "The credentials are expired or malformed: regenerate them with `ytmusicapi browser`."
            ) from error


def _parse_song(raw_song: dict[str, Any]) -> LibraryTrack | None:
    title = raw_song.get("title")
    if not isinstance(title, str):
        return None
    else:
        return LibraryTrack(
            video_id=_optional_string(raw_song.get("videoId")),
            title=title,
            artists=_parse_artists(raw_song.get("artists")),
            album_name=_parse_album_name(raw_song.get("album")),
        )


def _parse_removal_token(raw_song: dict[str, Any]) -> str | None:
    feedback_tokens = raw_song.get("feedbackTokens")
    if isinstance(feedback_tokens, dict):
        return _optional_string(feedback_tokens.get("remove"))
    else:
        return None


def _parse_artists(raw_artists: object) -> tuple[TrackArtist, ...]:
    if not isinstance(raw_artists, list):
        return ()
    else:
        return tuple(
            TrackArtist(name=artist["name"], channel_id=_optional_string(artist.get("id")))
            for artist in raw_artists
            if isinstance(artist, dict) and isinstance(artist.get("name"), str)
        )


def _parse_album_name(raw_album: object) -> str | None:
    if isinstance(raw_album, dict):
        return _optional_string(raw_album.get("name"))
    else:
        return None


def _optional_string(value: object) -> str | None:
    if isinstance(value, str):
        return value
    else:
        return None
