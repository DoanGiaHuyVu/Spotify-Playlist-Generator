import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "206b58280ed547e9b72d8a7ef94e37ba"
CLIENT_SECRET = "921451ac962145aabe6317d870b73edc"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="http://example.com",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    show_dialog=True,
    cache_path="token.txt",
    username="HyukJay"))

user_id = sp.current_user()["id"]
# print(user_id)
date_and_time = input("Which year do you want to travel to? "
                      "Type the date in this format YYYY-MM-DD: ")
URL = "https://www.billboard.com/charts/hot-100/" + date_and_time
response = requests.get(url=URL)
spotify_page = response.text

soup = BeautifulSoup(spotify_page, "html.parser")
songs = soup.select("li ul li h3")
song_titles = [song.getText().strip() for song in songs]
print(song_titles)

song_uris = []
song_ids = []
year = date_and_time.split("-")[0]
playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{date_and_time} BILLBOARD 100",
                                   public=False,
                                   collaborative=False,
                                   description=f"Top 100 on {date_and_time}")
# print(playlist["id"])
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_id = result["tracks"]["items"][0]["id"]
        # print(uri)
        # print(song_id)
        song_uris.append(uri)
        song_ids.append(song_id)

    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

add_tracks_to_playlist = sp.playlist_add_items(playlist_id=playlist["id"],items=song_uris, position=None )
