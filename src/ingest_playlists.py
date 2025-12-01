from datetime import datetime, timezone
import pandas as pd
from .spotify_client import get_spotify_client

PLAYLISTS = [
    {
        "id": "37i9dQZEVXbMDoHDwVN2tF?si=eeb9eadcf5a44868",  # Top 50 Global
        "region": "global",
        "playlist_type": "top50",
        "name": "Top 50 Global",
    }
    {
        "id": "37i9dQZEVXbLiRSasKsNU9?si=f0943b991ae34e64",  # Viral 50 Global
        "region": "global",
        "playlist_type": "viral50",
        "name": "Viral 50 Global",
    }
]

def fetch_playlist_tracks_snapshot(playlist_meta):
    sp = get_spotify_client()
    playlist_id = playlist_meta["id"]

    items = []
    limit = 100
    offset = 0

    while True:
        response = sp.playlist_items(
            playlist_id,
            limit=limit,
            offset=offset,
            additional_types=["track"]
        )
        batch = response.get("items", [])
        if not batch:
            break
        items.extend(batch)
        if len(batch) < limit:
            break
        offset += limit

    snapshot_ts = datetime.now(timezone.utc)

    rows = []
    for item in items:
        track = item.get("track")
        if track is None:
            continue

        rows.append({
            "snapshot_ts": snapshot_ts,
            "playlist_id": playlist_id,
            "playlist_name": playlist_meta["name"],
            "region": playlist_meta["region"],
            "playlist_type": playlist_meta["playlist_type"],
            "track_id": track.get("id"),
            "track_name": track.get("name"),
            "popularity": track.get("popularity"),
            "duration_ms": track.get("duration_ms"),
            "explicit": track.get("explicit")
        })

    return pd.DataFrame(rows)


def add_audio_features(df):
    sp = get_spotify_client()

    ids = df["track_id"].dropna().unique().tolist()
    features = []
    for i in range(0, len(ids), 100):
        batch = ids[i:i+100]
        features.extend(sp.audio_features(batch))

    feats_df = pd.DataFrame([f for f in features if f])
    return df.merge(feats_df, left_on="track_id", right_on="id", how="left")


def ingest_single_playlist_snapshot(playlist_meta):
    df = fetch_playlist_tracks_snapshot(playlist_meta)
    if df.empty:
        return df
    return add_audio_features(df)
