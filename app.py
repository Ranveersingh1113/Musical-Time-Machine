import os
from datetime import datetime
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from billboard_time_machine import (
    fetch_billboard_page,
    fetch_song_and_artist
)

# Load secrets
CLIENT_ID     = st.secrets["SPOTIPY"]["CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIPY"]["CLIENT_SECRET"]
REDIRECT_URI  = st.secrets["SPOTIPY"]["REDIRECT_URI"]
SCOPE         = "playlist-modify-private"

# UI
st.set_page_config(page_title="🎵 Musical Time Machine")
st.title("🎵 Musical Time Machine")
st.markdown("Pick a date in history and get a curated Spotify playlist of that day’s Hot‑100!")

# Date input
date_input = st.date_input("Select a date", value=datetime.today(), min_value=datetime(1958, 8, 4), max_value=datetime.today())

# Step 1: Get Auth URL
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path="token.txt",
    show_dialog=True,
    open_browser=False
)
auth_manager.state = None
auth_url = auth_manager.get_authorize_url()
st.markdown(f"[🔑 Click here to authorize Spotify]({auth_url})")

# Step 2: Ask for redirected URL
redirect_response = st.text_input("Paste the full redirect URL you were sent to after Spotify login")

# Step 3: Handle token exchange
if redirect_response:
    try:
        token_info = auth_manager.get_access_token(redirect_response)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        st.success("✅ Spotify authorized successfully!")

        # Run playlist generation
        target_date = date_input.strftime("%Y-%m-%d")
        soup = fetch_billboard_page(target_date)
        titles, artists = fetch_song_and_artist(soup)

        uris = []
        for title, artist in zip(titles, artists):
            query = f"track:{title} artist:{artist}"
            res   = sp.search(q=query, type="track", limit=1)
            items = res.get("tracks", {}).get("items")
            if items:
                uris.append(items[0]["uri"])

        user_id = sp.current_user()["id"]
        playlist = sp.user_playlist_create(
            user=user_id,
            name=f"{date_input.year} Billboard Hot‑100",
            public=False
        )
        sp.playlist_add_items(playlist_id=playlist["id"], items=uris)

        st.success(f"✅ Created “{playlist['name']}” with {len(uris)} tracks!")
        st.markdown(f"[🎧 Open in Spotify]({playlist['external_urls']['spotify']})")

    except Exception as e:
        st.error(f"❌ Error: {e}")
