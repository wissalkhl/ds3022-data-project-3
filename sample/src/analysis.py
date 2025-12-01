import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .config import DUCKDB_PATH

def load_data() -> pd.DataFrame:
    con = duckdb.connect(DUCKDB_PATH)
    df = con.execute("SELECCT * FROM spotify_tracks").df()
    con.close()
    return df

def plot_popularity_by_region(df: pd.DataFrame):
    plt.figure()
    sns.boxplot(data=df, x="region", y="popularity")
    plt.title("Popularity disctibution by region")
    plt.tight_layout()
    plt.savefig("plots/popularity_by_region.png")

def plot_duration_vs_popularity(df: pd.DataFrame):
    plt.figure()
    sms.scatterplot(data=df.sample(min(5000, len(df))), x="duration_ms", y="popularity", hue="region", alpha=0.5)
    plt.title("Duration vs Popularity by Region")
    plt.tight_layout()
    plt.savefig("plots/duration_vs_popularity.png")

if __name__ == "__main__":
    df = load_data()
    plot_popularity_by_region(df)
    plot_duration_vs_popularity(df)

