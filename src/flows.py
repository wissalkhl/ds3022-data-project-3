import pandas as pd
import duckdb
from prefect import flow, task

from .ingest_playlists import PLAYLISTS, ingest_single_playlist_snapshot
from .config import DUCKDB_PATH

@task
def ingest_playlist_task(meta):
    df = ingest_single_playlist_snapshot(meta)
    print(f"Ingested {len(df)} rows from {meta['name']}")
    return df

@task
def write_to_duckdb(dfs):
    dfs = [df for df in dfs if not df.empty]
    if not dfs:
        print("No dataframes to write.")
        return

    full_df = pd.concat(dfs)
    con = duckdb.connect(DUCKDB_PATH)

    con.execute("CREATE TABLE IF NOT EXISTS spotify_tracks AS SELECT * FROM full_df LIMIT 0;")
    con.execute("INSERT INTO spotify_tracks SELECT * FROM full_df;")
    con.close()

@flow
def daily_spotify_snapshot_flow():
    futures = []
    for meta in PLAYLISTS:
        futures.append(ingest_playlist_task.submit(meta))

    results = [f.result() for f in futures]
    write_to_duckdb(results)

if __name__ == "__main__":
    daily_spotify_snapshot_flow()
