# PlexScripts

The script consists of 3 files:

* plex_config.py <br />
  ```This is where you will add your settings that the two scripts will use```
* Unwatched.py <br />
  ```A script that will add first unwatched episode of a given plex collection to a playlist, and randomize the playlist```
* Reruns.py <br />
  ```A script that will add previoulsy watched episodes of a given plex collection to a playlist, and randomize the playlist```


# plex_config.py
This is where you will add your settings that the two scripts will use

PLEX_URL = http://x.x.x.x:32400 ```url of your plex server``` <br />
PLEX_TOKEN = 123ABcdEf567 ```url of your plex server```<br />
NUMBER_OF_SHOWS = 5 ```total number of episodes that will be in the final playlist```<br />
NUMBER_OF_DAYS_TO_NOT_RERUN = 30 ```if a episode was already played in the past xx days, it wont be added```<br />
# 
