# Update these:
# The name of the Collection of shows in Plex
COLLECTION_NAME = 'Current Shows'
# The name of the wanted playlist in Plex
MY_PLAYLIST = 'Single Stream'
# The name of the Library in Plex
LIBRARY_NAME = 'TV Shows'

import os
import datetime
import random
from plexapi.server import PlexServer
import configparser

# Import settings
plex_config = configparser.ConfigParser()
plex_config.read("plex_config.ini")
baseurl = plex_config.get('plex_config', 'PLEX_URL')
token = plex_config.get('plex_config', 'PLEX_TOKEN')
NUMBER_OF_EP_OVERRIDE = 0

plex = PlexServer(baseurl, token)
tv_shows_section = plex.library.section(LIBRARY_NAME)

# CODE
# Check if playlist exists, if it does, remove so that it can be repopulated
for playlist in plex.playlists():
    if playlist.title == MY_PLAYLIST:
        print('{} already exists. Deleting and rebuilding.'.format(MY_PLAYLIST))
        playlist.delete()

show_weighted_episodes = {}

for collection in tv_shows_section.collection(COLLECTION_NAME):
    tv_show = collection.title

    # Skip this show if we've already added an episode from it
    if tv_show in show_weighted_episodes:
        continue

    all_seasons = plex.library.section(LIBRARY_NAME).get(tv_show).seasons()
    for season in all_seasons:
        all_eps = season.episodes()
        for episode in all_eps:
            if not episode.isWatched:
                last_watched_at = episode.lastViewedAt or datetime.datetime.min
                time_since_watched = datetime.datetime.now() - last_watched_at
                weight = time_since_watched.total_seconds()
                
                # Store the episode and its weight, keyed by the show's title
                show_weighted_episodes[tv_show] = (episode, weight)
                break
        if tv_show in show_weighted_episodes:
            break  # Break if we've added an episode for this show

def weighted_show_selection(shows, num_selections):
    selected_episodes = []
    while len(selected_episodes) < num_selections and shows:
        total_weight = sum(weight for show, (episode, weight) in shows.items())
        if total_weight == 0:
            break  # Avoid division by zero

        r = random.uniform(0, total_weight)
        upto = 0
        for show, (episode, weight) in shows.items():
            if upto + weight >= r:
                selected_episodes.append(episode)
                del shows[show]  # Remove this show from the dictionary
                break
            upto += weight

    return selected_episodes

if NUMBER_OF_EP_OVERRIDE <= 0:
    NUMBER_OF_EP_OVERRIDE = len(show_weighted_episodes)
    print(f"Setting NUMBER_OF_EP_OVERRIDE to the number of unique shows: {NUMBER_OF_EP_OVERRIDE}")

# Perform weighted selection without replacement
final_playlist = weighted_show_selection(show_weighted_episodes, NUMBER_OF_EP_OVERRIDE)

print(f'Adding {len(final_playlist)} shows to playlist.')
if final_playlist:
    plex.createPlaylist(MY_PLAYLIST, items=final_playlist)
else:
    print("No unwatched episodes available to add to the playlist.")
