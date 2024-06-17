import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-modify-playback-state user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_id="",    # insert client id here
    client_secret="", # insert client secret here
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


def player_available():
    if len(sp.devices()["devices"]) <= 0 or not sp.devices()["devices"][0]["is_active"]:
        return False
    else:
        return True


def pause():
    if player_available():
        sp.pause_playback()


def resume():
    if player_available():
        sp.start_playback()


def forward():
    if player_available():
        sp.next_track()


def back():
    if player_available():
        sp.previous_track()


def is_currently_playing():
    try:
        return sp.current_playback()["is_playing"]
    except TypeError:
        return None


if __name__ == '__main__':
    print(sp.devices()["devices"][0]["is_active"])


# print(f"{name} - {', '.join(artists)}")
