from pprint import pprint

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


ID = "SPOTIFY_ID"
SECRET = "SPOTIFY SECRET"


date = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")

URL = "https://www.billboard.com/charts/hot-100/" + date + '/'

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

class_name = "c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"

titles = soup.select("li #title-of-a-story")

song_names = [title.getText().strip() for title in titles]
#print(song_names)

#creating Spotify access
scope = "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=ID,
        client_secret=SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

year = date.split("-")[0]
user_id = sp.current_user()["id"]
song_uris = []
for song in song_names:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = result["tracks"]['items'][0]['uri']
        song_uris.append(uri)
    except:
        print(f"{song} doesn't exist in Spotify. Skipped.")
      
#print(song_uris)
playlist = sp.user_playlist_create(user=user_id, name=f"Top 100 Billboard songs on {date}", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
