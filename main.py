from bs4 import BeautifulSoup
import requests as r
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from dotenv import load_dotenv
import os

scope = "playlist-modify-private"
load_dotenv()  # reads .env into os.environ
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
CACHE_PATH = os.getenv("SPOTIPY_CACHE_PATH")
USERNAME = os.getenv("SPOTIPY_USERNAME")

def fetch_billboard_page(year: str) -> BeautifulSoup:
    header = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )
    }
    response = r.get(
        url=f"https://www.billboard.com/charts/hot-100/{year}",
        headers=header
    )
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def fetch_song_and_artist(soup: BeautifulSoup):
    songs = soup.select("div ul li ul li h3")
    song_names = [song.getText().strip() for song in songs]

    artists = soup.find_all(name="span", class_="a-font-primary-s")
    t100_artist = [artist.getText().strip("\n\t") for artist in artists]

    # remove stray certification labels
    t100_artist = [a for a in t100_artist if a != "RIAA Certification:"]

    return song_names, t100_artist


def create_spotify_connection(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    scope: str,
    cache_path: str = "token.txt",
    show_dialog: bool = True
) -> Spotify:
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=cache_path,
        show_dialog=show_dialog,
        open_browser = False
        
    )
    return Spotify(auth_manager=auth_manager)


if __name__ == "__main__":
    year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
    date_prefix = year.split("-")[0]

    # 1) Fetch and parse Billboard page
    soup = fetch_billboard_page(year)
    song_names, t100_artist = fetch_song_and_artist(soup)

    # 2) Authenticate with Spotify
    sp = create_spotify_connection()
    user_id = sp.current_user()["id"]

    # 3) Search each track and collect URIs
    song_uris = []
    for song in song_names:
        result = sp.search(q=f"track:{song}", type="track", limit=1)
        print(result)
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

    # 4) Create a new private playlist
    playlist = sp.user_playlist_create(
        user=user_id,
        name=f"{date_prefix} Billboard 100",
        public=False
    )

    # 5) Add all found songs to the playlist
    sp.playlist_add_items(
        playlist_id=playlist["id"],
        items=song_uris
    )

    print(f"✅ Created playlist '{date_prefix} Billboard 100' with {len(song_uris)} tracks!")
