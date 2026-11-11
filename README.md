# YTMusic library AI scanner

Lists the songs of your YouTube Music library whose artist is reported as publishing AI-generated music in the [SoundProof](https://github.com/NuclearBlox/SoundProof-Dumps) community database.

## Installation

Python 3.10 or newer, then:

```bash
pip install ytmusicapi
```

## YouTube Music cookies

1. Open https://music.youtube.com, logged in to your account.
2. Open the developer tools (`F12`), **Network** tab, and filter on `browse`.
3. Click **Library** in YouTube Music, then on a `POST` `browse` request (status `200`).
4. Copy its **request headers** in raw mode (*Raw*). The block must contain `cookie:` and `x-goog-authuser:`.
5. At the root of the project, run `ytmusicapi browser`, paste the headers, then finish with `Enter`, `Ctrl+Z`, `Enter` (Windows) or `Ctrl+D` (Linux / macOS).

This creates `browser.json`, which grants access to your account: do not share it (it is ignored by git).

## Usage

```bash
python main.py
python main.py --force # list artists with at least one AI vote
```

The CSV report (`report.csv`) lists the tracks having an artist with `AI votes >= human votes`.  

You can use the `--delete` flag (/!\ **destructive**) to remove the tracks listed in `report.csv` from your YouTube Music library. It's recommended to review (and edit) the report before deleting any tracks.
