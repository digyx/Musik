# Musik

Syncs Spotify queues with a server so multiple people can listen to the same songs at the same time.  The server application uses a CLI that can allow the user to select a playlist, choose which songs to add to the queue, shuffle the queue, pause playback, and more.

All a user needs to do is:
1. Have the host set the server up
1. Start playing a song via Spotify
1. Open the client application

### "Why not just use Discord?"
Discord's Spotify sharing does not allow you to chat over voice at the same time.

### "What commands are there?"
```
# List the playlist, with numbers
>> list

# Play all songs on the playlist
>> all

# Play specific song or songs
>> 3
>> 1 5 7

# Shuffle the queue
>> shuffle

# Pause playback on all devices
>> pause

# Clear the console
>> clear
```