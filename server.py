import asyncio
import websockets

from spotipy import Spotify
from spotipy.oauth2 import SpotifyPKCE

from params import Params

import time
from threading import Thread, Event

auth_manager = SpotifyPKCE(client_id="a9ed7f99384943dc98518ed396cd639a",
                            redirect_uri="http://localhost:7998/callback",
                            scope="playlist-read-private",
                            open_browser=False)

sp = Spotify(auth_manager=auth_manager)

event = Event()


async def handler(ws, path):
    event.wait()
    await ws.send(params.get_queue())


def start_server():    
    asyncio.set_event_loop(asyncio.new_event_loop())
    server = websockets.serve(handler, "0.0.0.0", 7999)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()


def init():
    # Determine which playlist to use
    playlists = sp.current_user_playlists()

    for index, entry in enumerate(playlists['items'], start=1):
        print("{} : {}".format(index, entry['name']))

    index = int(input("Which playlist? ")) - 1
    playlist_uri = playlists['items'][index]['uri']

    return Params(playlist_uri, sp)

def track_manager():
    global params
    params = init()

    while True:
        params.set_queue()

        # Sync song changes
        if params.change():
            event.clear()
            time.sleep(2)
            event.set()


server = Thread(target=start_server, args=())
tracks = Thread(target=track_manager, args=())

server.start()
tracks.start()

server.join()
tracks.join()
