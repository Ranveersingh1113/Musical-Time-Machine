# 🎵 Musical Time Machine

> Travel back in time and generate a Spotify playlist of Billboard's Hot 100 from any date since 1958.

---

## 📸 Preview

![musical-time-machine-demo](https://github.com/your-username/musical-time-machine/assets/demo.gif)
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
git clone https://github.com/your-username/musical-time-machine.git
cd musical-time-machine
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
