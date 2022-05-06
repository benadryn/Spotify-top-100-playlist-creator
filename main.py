import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv("H:/Python/.env")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

date = input("Which year do you want to travel to? YYYY-MM-DD: ")
year = date.split("-")[0]
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
hot_100_web = response.text

soup = BeautifulSoup(hot_100_web, "html.parser")


list_of_song_names = []
song_names_ugly = soup.select("h3.c-title.a-no-trucate.a-font-primary-bold-s")
song_names = [title.getText().split() for title in song_names_ugly]

for song_name in song_names:
    list_of_song_names.append(" ".join(song_name))

song_uris = []
scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                               scope=scope,
                                               redirect_uri="https://open.spotify.com/collection/playlists"))

user_id = sp.me()["id"]
new_playlist = sp.user_playlist_create(user_id, f"{date} Billboard 100")
for song in list_of_song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")

sp.playlist_add_items(new_playlist["id"], song_uris)
