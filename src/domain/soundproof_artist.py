from dataclasses import dataclass




@dataclass(frozen=True)
class SoundProofArtist:
    """One artist entry of the SoundProof community database."""

    identifier: str
    name: str
    verified: bool
    ai_votes: int
    human_votes: int
