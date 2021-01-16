from spotipy import Spotify
from spotipy.oauth2 import SpotifyPKCE

import asyncio, websockets, time
import platform, subprocess


auth_manager = SpotifyPKCE(client_id="a9ed7f99384943dc98518ed396cd639a",
                            redirect_uri="http://localhost:7999/callback",
                            scope="streaming")

sp = Spotify(auth_manager=auth_manager)


def play(uri: str):
    sp.start_playback(uris=[uri])
    sp.repeat("track")


def pause():
    sp.pause_playback()


def print_track(track):
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

    print("Now playing:")
    print("\tName.....", track['name'])
    print("\tAlbum....", track['album']["name"])
    print("\tArtists..", end=" ")

    for artist in track["album"]["artists"]:
        print(artist["name"], end=", ")
    print()


async def client():
    uri = "ws://api.vorona.gg:7999"
    now_playing = ""

    print("Connecting to server...")

    while True:
        async with websockets.connect(uri) as ws:
            try:
                track_uri = await ws.recv()
            except:
                print("There was an error.  Shame.")
    
            if track_uri == now_playing:
                time.sleep(1)
                continue
            else:
                play(track_uri)
                now_playing = track_uri

                print_track(sp.track(track_uri))


asyncio.get_event_loop().run_until_complete(client())
