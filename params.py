from spotipy import Spotify
from random import shuffle

import subprocess

class Params:
    def __init__(self, 
            playlist_id: str, 
            spotify: Spotify):
        
        self.spotify = spotify
        self.playlist_id = playlist_id

        self.__change = False
        self.__queue = self.get_tracks()
        self.__playlist = self.get_tracks()


    def change(self):
        return self.__change


    def get_queue(self):
        return str(self.__queue)


    def set_queue(self):
        self.__change = False
        selection = input(">> ")

        if selection == "all":
            self.__queue = [i['track']['uri'] for i in self.__playlist]
            self.__change = True

        elif selection == "shuffle":
            shuffle(self.__queue)
            self.__change = True
        
        elif selection == "pause":
            self.__queue = ["pause"]
            self.__change = True

        elif selection == "list":
            self.get_tracks(log=True)

        elif selection == "clear":
            subprocess.run("clear", shell=True)
        
        else:
            self.__queue = []
            for i in [int(i) - 1 for i in selection.split(" ")]:
                self.__queue.append(self.__playlist[i]["track"]["uri"])


    def get_tracks(self, log=False):
        playlist = self.spotify.playlist_items(self.playlist_id)["items"]
        
        if log:
            for i, track in enumerate(playlist, start=1):
                track = track["track"]
                print("{} : {}, {}".format(i, track["name"], track["album"]["name"]))

        return playlist
