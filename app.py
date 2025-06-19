import os
from datetime import datetime

import streamlit as st
#from dotenv import load_dotenv
from main import (
    fetch_billboard_page,
    fetch_song_and_artist,
    create_spotify_connection
)

# ─── Load Secrets ───

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
CACHE_PATH = os.getenv("SPOTIPY_CACHE_PATH")
USERNAME = os.getenv("SPOTIPY_USERNAME")

# ─── UI Header ───
st.set_page_config(page_title="🎵 Musical Time Machine")
st.title("🎵 Musical Time Machine")
st.markdown(
    "Pick a date in history and get a curated Spotify playlist of that day’s Hot‑100!"
)

# ─── Date Picker ───
date_input = st.date_input(
    "Select a date",
    value=datetime.today(),
    min_value=datetime(1958, 8, 4),
    max_value=datetime.today()
)

# ─── Generate Button ───
if st.button("Generate Playlist"):
    # Format date
    target_date = date_input.strftime("%Y-%m-%d")

    try:
        # 1) Scrape Billboard
        soup = fetch_billboard_page(target_date)
        titles, artists = fetch_song_and_artist(soup)

        # 2) OAuth & Spotify client
        sp = create_spotify_connection()
        user_id = sp.current_user()["id"]

        # 3) Search & collect URIs
        uris = []
        for title, artist in zip(titles, artists):
            query = f"track:{title} artist:{artist}"
            res   = sp.search(q=query, type="track", limit=1)
            items = res.get("tracks", {}).get("items")
            if items:
                uris.append(items[0]["uri"])

        # 4) Create Playlist & Add Tracks
        playlist = sp.user_playlist_create(
            user = user_id,
            name = f"{date_input.year} Billboard Hot‑100",
            public = False
        )
        sp.playlist_add_items(playlist_id=playlist["id"], items=uris)

        # 5) Show Success
        st.success(f"✅ Created “{playlist['name']}” with {len(uris)} tracks!")
        st.markdown(f"[Open in Spotify]({playlist['external_urls']['spotify']})")

    except Exception as e:
        st.error(f"❌ Error: {e}")

        
