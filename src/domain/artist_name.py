import unicodedata




def normalize_artist_name(name: str) -> str:
    """Build the key used to match an artist name between YouTube Music and SoundProof.

    NFKC folds typographic variants (full-width letters, ligatures) and casefold handles case-insensitive matching beyond ASCII, so "ＤＡＦＴ  Punk" and "daft punk" share one key.
    """
    folded_name = unicodedata.normalize("NFKC", name).casefold()
    return " ".join(folded_name.split())
