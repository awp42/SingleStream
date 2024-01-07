# Single Stream
A tool for deciding what to watch on plex. 

* RandomUnwatched.py
  ```A script that will add first unwatched episode of a given plex collection to a playlist, episodes are weighted based on time since watching and then randomly selected```

# plex_config.py
PLEX_URL = http://x.x.x.x:32400 ```url of your plex server``` <br />
PLEX_TOKEN = 123ABcdEf567 ```Token of your plex server```<br />
NUMBER_OF_SHOWS = 5 ```total number of episodes that will be in the final playlist```<br />
NUMBER_OF_DAYS_TO_NOT_RERUN = 30 ```if a episode was already played in the past xx days, it wont be added (used for rerun.py)```<br />
<br />
# RandomUnwatched.py
The following can be changed in the script
<br />
<br />
COLLECTION_NAME = 'Current Shows' ```name of the collection in Plex that is to be used to populate the playlists``` <br />
MY_PLAYLIST = 'Single Stream' ```The name of the playlist that will be created``` <br />
LIBRARY_NAME = 'TV Shows' ```The name of the library where the TV Shows are located in Plex``` <br />
NUMBER_OF_EP_OVERRIDE = '0' ```This can be changed to limit the number of shows that will be on the playlist. By default the list will continue one entry for each show within the collection``` <br />
<br />

