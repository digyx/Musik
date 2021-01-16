import asyncio
import websockets

from spotipy import Spotify
from spotipy.oauth2 import SpotifyPKCE

import time, subprocess
from threading import Thread, Event

auth_manager = SpotifyPKCE(client_id="a9ed7f99384943dc98518ed396cd639a",
                            redirect_uri="http://localhost:8000/callback",
                            scope="playlist-read-private",
                            open_browser=False)

sp = Spotify(auth_manager=auth_manager)
track_uri = "spotify:track:4gCnaT6NKQmR3hqEeHp30t"
playlist = sp.playlist_items("6W3d5DZZ09QfEsPP8khAWw")

event = Event()


async def handler(ws, path):
    event.wait()
    await ws.send(track_uri)


def start_server():    
    asyncio.set_event_loop(asyncio.new_event_loop())
    server = websockets.serve(handler, "0.0.0.0", 8080)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()


def get_tracks():
    global playlist

    i = 1
    for i, track in enumerate(playlist["items"], start=1):
        track = track["track"]
        print("{} : {}, {}".format(i, track["name"], track["album"]["name"]))


def track_manager():
    while True:
        subprocess.run("clear", shell=True)
        get_tracks()

        global playlist
        global track_uri

        track_selection = int(input("Selection: "))
        track_uri = playlist["items"][track_selection - 1]["track"]["uri"]

        # Sync song changes
        event.clear()
        time.sleep(2)
        event.set()


server = Thread(target=start_server, args=())
tracks = Thread(target=track_manager, args=())

server.start()
tracks.start()

server.join()
tracks.join()
