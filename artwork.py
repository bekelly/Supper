# artwork.py

import hashlib
from pathlib import Path
import requests

# 1) Cache directory is located alongside this file
BASE_DIR  = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# iTunes API endpoints
ITUNES_SEARCH = "https://itunes.apple.com/search"
ITUNES_LOOKUP = "https://itunes.apple.com/lookup"
COUNTRY       = "us"


def _hash_metadata(artist: str, album: str) -> str:
    """
    Create a filesystem-safe, unique filename from artist/album.
    """
    key = f"{artist}|{album}".lower().strip()
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()
    return f"{digest}.jpg"


def _fetch_artist_id(artist: str) -> int:
    """
    Lookup the artist in iTunes and return their numeric artistId.
    """
    params = {
        "term":    artist,
        "entity":  "musicArtist",
        "limit":   1,
        "country": COUNTRY,
    }
    resp = requests.get(ITUNES_SEARCH, params=params, timeout=5)
    resp.raise_for_status()

    results = resp.json().get("results", [])
    if not results:
        raise FileNotFoundError(f"No iTunes artist match for '{artist}'")

    return results[0]["artistId"]


def _download_artwork_itunes(artist: str, album: str) -> bytes:
    """
    Two-step iTunes download:
      1) Fetch artistId
      2) Lookup all albums by that artist
      3) Exact-match collectionName to album, then grab artworkUrl100 → 600×600
    Raises FileNotFoundError if no exact album match.
    """
    # 1) Get the artistId
    artist_id = _fetch_artist_id(artist)

    # 2) Lookup all albums for this artist
    params = {
        "id":      artist_id,
        "entity":  "album",
        "limit":   200,
        "country": COUNTRY,
    }
    resp = requests.get(ITUNES_LOOKUP, params=params, timeout=5)
    resp.raise_for_status()

    # The first item is the artist record; the rest are albums
    albums = resp.json().get("results", [])[1:]

    # 3) Find the exact album match
    target = album.lower().strip()
    for entry in albums:
        name = entry.get("collectionName", "").lower().strip()
        if name == target:
            art_url = entry.get("artworkUrl100")
            if not art_url:
                raise FileNotFoundError(f"No artwork URL for '{artist} – {album}'")

            # Upgrade 100×100 → 600×600
            hi_res_url = art_url.replace("100x100", "600x600")
            img_resp   = requests.get(hi_res_url, timeout=5)
            img_resp.raise_for_status()
            return img_resp.content

    raise FileNotFoundError(f"No exact iTunes album match for '{artist} – {album}'")


def _download_artwork_caa(artist: str, album: str) -> bytes:
    """
    MusicBrainz / Cover Art Archive fallback:
      1) Search release-group for artist AND album
      2) Fetch /front-600.jpg for that MBID
    """
    # 1) Find the release-group MBID
    query = f'artist:"{artist}" AND release:"{album}"'
    mb_url = "https://musicbrainz.org/ws/2/release-group"
    resp   = requests.get(
        mb_url,
        params={"query": query, "fmt": "json", "limit": 1},
        timeout=5
    )
    resp.raise_for_status()

    items = resp.json().get("release-groups", [])
    if not items:
        raise FileNotFoundError(f"No MusicBrainz release-group for '{artist} – {album}'")

    mbid = items[0]["id"]

    # 2) Download cover art front-600.jpg
    cover_url = f"https://coverartarchive.org/release-group/{mbid}/front-600.jpg"
    img_resp  = requests.get(cover_url, timeout=5)
    img_resp.raise_for_status()
    return img_resp.content


def get_artwork(artist: str, album: str) -> Path:
    """
    Returns Path to a local JPG file in cache/.
    If missing:
      1) Try iTunes two-step lookup
      2) On failure, try CAA fallback
      3) On final failure, return assets/fallback.png
    """
    # Compute cache filename + path
    fname = _hash_metadata(artist, album)
    path  = CACHE_DIR / fname

    # 2) Cache hit?
    if path.exists():
        print(f"[artwork] cache hit: {path.name}")
        return path

    # 3) Cache miss — attempt downloads
    print(f"[artwork] cache miss: downloading '{artist} – {album}'")
    try:
        img_bytes = _download_artwork_itunes(artist, album)
        path.write_bytes(img_bytes)
        print(f"[artwork] saved to cache: {path.name}")
        return path

    except FileNotFoundError as e:
        print(f"[artwork] iTunes failed: {e}")

        try:
            img_bytes = _download_artwork_caa(artist, album)
            path.write_bytes(img_bytes)
            print(f"[artwork] CAA fallback succeeded: {path.name}")
            return path

        except Exception as ee:
            print(f"[artwork] CAA fallback failed: {ee}")
            return Path("assets/fallback.png")


# Example CLI test
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python artwork.py \"Artist Name\" \"Album Name\"")
        sys.exit(1)

    artist = sys.argv[1]
    album  = sys.argv[2]
    out    = get_artwork(artist, album)
    print("Artwork returned:", out)