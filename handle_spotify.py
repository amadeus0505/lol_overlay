import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "app-remote-control user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_id="e9850e038b60444cbb56d51c2b8ca46d",
    client_secret="ea1247fa80884997b48ccfd12c59c82f",
    redirect_uri="http://localhost:8888"
))


def get_current_track():
    try:
        name = sp.current_user_playing_track()["item"]["name"]
        artists = []
    except TypeError:
        return "No Track Running", ""

    for artist in sp.current_user_playing_track()["item"]["artists"]:
        artists.append(artist["name"])

    return name, artists

if __name__ == '__main__':
    print(get_current_track())

# print(f"{name} - {', '.join(artists)}")