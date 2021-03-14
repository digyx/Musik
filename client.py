from spotipy import Spotify
from spotipy.oauth2 import SpotifyPKCE

import asyncio, websockets, time, ast
import platform, subprocess


auth_manager = SpotifyPKCE(client_id="a9ed7f99384943dc98518ed396cd639a",
                            redirect_uri="http://localhost:7998/callback",
                            scope="streaming user-read-playback-state user-modify-playback-state")

sp = Spotify(auth_manager=auth_manager)
device_id = sp.current_playback()['device']['id']

def play(uris: str):
    sp.start_playback(uris=uris, device_id=device_id)
    sp.repeat("context", device_id=device_id)
    sp.shuffle(False, device_id=device_id)


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
                track_uris = await ws.recv()
                print("\rConnected and playing.", end="")
            except:
                print("\rError....", end="")
    
            if track_uris == now_playing:
                time.sleep(1)
                continue
            elif track_uris == "['pause']":
                pause()
                now_playing = track_uris
                print("\rPaused.", end="")
            else:
                play(ast.literal_eval(track_uris))
                now_playing = track_uris


asyncio.get_event_loop().run_until_complete(client())
