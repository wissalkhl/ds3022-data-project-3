import duckdb
from .config import DUCKDB_PATH

def init_duckdb():
    con = duckdb.connect(DUCKDB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS spotify_tracks (
            snapshot_ts TIMESTAMP,
            playlist_id VARCHAR,
            playlist_name VARCHAR,
            playlist_type VARCHAR,
            track_id VARCHAR,
            track_name VARCHAR,
            popularity INTEGER,
            duration_ms BIGINT,
            explicit BOOLEAN
        );
    """)
    con.close()

