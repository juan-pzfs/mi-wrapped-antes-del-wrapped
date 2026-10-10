from pathlib import Path
import pandas as pd

# 👇 Para cambiar a datos reales, solo cambia esta línea
CARPETA = Path("sample_data/Spotify Extended Streaming History")


def cargar_historial(carpeta):
    """Lee todos los archivos de historial de una carpeta y los junta en una tabla."""
    archivos = sorted(carpeta.glob("Streaming_History_Audio_*.json"))
    print(f"Archivos encontrados: {len(archivos)}")
    tablas = [pd.read_json(archivo) for archivo in archivos]
    return pd.concat(tablas, ignore_index=True)

def limpiar(df):
    """Deja solo música escuchada de verdad, con las columnas que necesitamos."""
    df = df[df["master_metadata_track_name"].notna()]   # quitar podcasts y audiolibros
    df = df[df["ms_played"] >= 30_000]                    # 30+ segundos = cuenta como "stream"
    df = df.rename(columns={
        "master_metadata_track_name": "cancion",
        "master_metadata_album_artist_name": "artista",
    })
    df = df[["ts", "ms_played", "cancion", "artista"]].copy()
    df["ts"] = pd.to_datetime(df["ts"])
    return df


if __name__ == "__main__":
    df = cargar_historial(CARPETA)
    print("Antes de limpiar:", df.shape)
    df = limpiar(df)
    print("Después de limpiar:", df.shape)
    print(df.head())