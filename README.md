# Single Stream
A tool for deciding what to watch on plex. 

# Unraid Setup
1. Install NerdPack GUI
2. Enable Python3 
3. Enable Python pip 
4. Create /user/mnt/script ```mkdir -p /mnt/user/scripts``` 
5. Save RandomUnwatched.py / plex_config.ini to scripts
6. Configure per the below
7. Run script in Unraid console ```cd /mnt/user/scripts``` then ```python3 RandomUnwatched.py```

# plex_config.py
PLEX_URL = http://x.x.x.x:32400 ```url of your plex server``` <br />
PLEX_TOKEN = 123ABcdEf567 ```Token of your plex server. Instructions to find [here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)```<br />
NUMBER_OF_SHOWS = 5 ```total number of episodes that will be in the final playlist```<br />
<br />
# RandomUnwatched.py
 ```A script that will add first unwatched episode of a given plex collection to a playlist, episodes are randomly selected based on a weighted value. The script will delete and recreate the Playlist each time it is run.```
 
The following can be changed in the script
<br />
<br />
COLLECTION_NAME = 'Current Shows' ```name of the collection in Plex that is to be used to populate the playlists``` <br />
MY_PLAYLIST = 'Single Stream' ```The name of the playlist that will be created``` <br />
LIBRARY_NAME = 'TV Shows' ```The name of the library where the TV Shows are located in Plex``` <br />
NUMBER_OF_EP_OVERRIDE = '0' ```This can be changed to limit the number of shows that will be on the playlist. By default the list will continue one entry for each show within the collection``` <br />
<br />

