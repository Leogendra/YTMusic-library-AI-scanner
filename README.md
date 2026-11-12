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

Output:
```bash
Analyzed 804 library tracks:
  AI                 5
  Tied votes         12
  Human              484
  Not in SoundProof  315
```

The CSV report (`report.csv`) lists the tracks having an artist with `AI votes >= human votes`.  

You can use the `--delete` flag (/!\ **destructive**) to remove the tracks listed in `report.csv` from your YouTube Music library. It's recommended to review (and edit) the report before deleting any tracks.

### Check the artists missing from SoundProof

The artists marked as "Not in SoundProof" in the console report are not in the community database yet, so they cannot be flagged. You can help the project by voting for them with the [SoundProof extension](https://github.com/NuclearBlox/SoundProof-extension). The `--check` mode helps you to pick which artists deserve a look first:

```bash
python main.py --check
```

It writes `check.csv` where these artists are ranked by a naive heuristic: AI profiles publish many releases in a short time, so the artists with the highest number of releases over the last two years come first.  
Disclaimer: this is only a greedy heuristic: a new human artist also has recent releases only, so review the top of the list by hand before voting.
