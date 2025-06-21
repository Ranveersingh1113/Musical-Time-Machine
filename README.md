# 🎵 Musical Time Machine

> Travel back in time and generate a Spotify playlist of Billboard's Hot 100 from any date since 1958.

---

## 📸 Preview

![musical-time-machine-demo](https://github.com/Ranveersingh1113/Musical-Time-Machine/assets/demo.gif)
> _(Replace this with your own GIF or screenshot of the app UI)_

---

## 📌 Features

- 🧭 Choose any date since **August 4, 1958**
- 🔥 Scrapes top 100 songs from Billboard Hot 100 chart for that day
- 🪄 Searches Spotify for each track
- 🎧 Creates a **private playlist** in your Spotify account
- 💚 Powered by `Spotipy`, `BeautifulSoup`, and `Streamlit` (optional)

---

## 🚀 Getting Started

### 🛠️ Prerequisites

- Python 3.8+
- A free [Spotify Developer](https://developer.spotify.com/dashboard) account
- A registered Spotify App (for API credentials)

---

## 🔑 Spotify App Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Under app settings:
   - Copy your **Client ID** and **Client Secret**
   - Add a redirect URI:
     - For CLI: `http://localhost:8888/callback`
     - For Streamlit local: `http://localhost:8501/`
4. Save the settings

---

## ⚙️ Installation

```bash
git clone https://github.com/Ranveersingh1113/Musical-Time-Machine.git
cd Musical-Time-Machine
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the root directory with the following keys:

```env
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8501/  # or http://localhost:8888/callback if using CLI
SPOTIPY_USERNAME=your_spotify_username
SPOTIPY_CACHE_PATH=token.txt
```

---

## 🖥️ Streamlit App (Optional)

```bash
streamlit run app.py
```

---

## 🧠 How It Works

| Step | Description                                   |
|------|-----------------------------------------------|
| 1️⃣  | Scrape Billboard Hot 100 using BeautifulSoup  |
| 2️⃣  | Extract song titles and artist names          |
| 3️⃣  | Use Spotipy to search Spotify for each song   |
| 4️⃣  | Authenticate user via Spotify OAuth           |
| 5️⃣  | Create playlist and add found songs           |

---

## 📦 Dependencies

- [spotipy](https://spotipy.readthedocs.io/) — Spotify Web API client
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing
- [streamlit](https://streamlit.io/) — Web interface (optional)
- [python-dotenv](https://github.com/theskumar/python-dotenv) — Load environment variables from `.env`

---

## ✨ Credits

Created by [Ranveersingh1113](https://github.com/Ranveersingh1113)

---

## 📄 License

This project is licensed under the MIT license

---
