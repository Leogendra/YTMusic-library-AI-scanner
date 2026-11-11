from enum import Enum




class ArtistStatus(Enum):
    """Verdict on whether an artist publishes AI-generated music."""

    AI = "ai"
    TIE = "tie"
    HUMAN = "human"
    UNKNOWN = "unknown"
