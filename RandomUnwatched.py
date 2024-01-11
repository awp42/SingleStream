import os
import datetime
import random
import logging
from plexapi.server import PlexServer
import configparser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_config():
    plex_config = configparser.ConfigParser()
    plex_config.read("plex_config.ini")
    return plex_config.get('plex_config', 'PLEX_URL'), plex_config.get('plex_config', 'PLEX_TOKEN')

def get_plex_server(baseurl, token):
    try:
        return PlexServer(baseurl, token)
    except Exception as e:
        logging.error(f"Error connecting to Plex Server: {e}")
        return None

def find_or_create_playlist(plex, playlist_name):
    for playlist in plex.playlists():
        if playlist.title == playlist_name:
            return playlist
    try:
        return plex.createPlaylist(playlist_name, items=[])
    except Exception as e:
        logging.error(f"Error creating playlist: {e}")
        return None

def get_unwatched_episodes(plex, library_name, collection_name):
    show_weighted_episodes = {}
    try:
        tv_shows_section = plex.library.section(library_name)
        for collection in tv_shows_section.collection(collection_name):
            process_collection(collection, show_weighted_episodes)
    except Exception as e:
        logging.error(f"Error processing collection: {e}")
    return show_weighted_episodes

def process_collection(collection, show_weighted_episodes):
    tv_show = collection.title
    if tv_show in show_weighted_episodes:
        return

    all_seasons = collection.seasons()
    for season in all_seasons:
        all_eps = season.episodes()
        for episode in all_eps:
            if not episode.isWatched:
                last_watched_at = episode.lastViewedAt or datetime.datetime.min
                time_since_watched = datetime.datetime.now() - last_watched_at
                weight = time_since_watched.total_seconds()
                show_weighted_episodes[tv_show] = (episode, weight)
                break
        if tv_show in show_weighted_episodes:
            break

def weighted_show_selection(shows, num_selections):
    selected_episodes = []
    while len(selected_episodes) < num_selections and shows:
        total_weight = sum(weight for show, (episode, weight) in shows.items())
        if total_weight == 0:
            break

        r = random.uniform(0, total_weight)
        upto = 0
        for show, (episode, weight) in shows.items():
            if upto + weight >= r:
                selected_episodes.append(episode)
                del shows[show]
                break
            upto += weight
    return selected_episodes

def update_playlist(playlist, episodes):
    try:
        playlist.removeItems(playlist.items())
        playlist.addItems(episodes)
    except Exception as e:
        logging.error(f"Error updating playlist: {e}")

def main():
    COLLECTION_NAME = 'Current Shows'
    MY_PLAYLIST = 'Single Stream'
    LIBRARY_NAME = 'TV Shows'
    NUMBER_OF_EP_OVERRIDE = 0

    baseurl, token = read_config()
    plex = get_plex_server(baseurl, token)
    if not plex:
        return

    existing_playlist = find_or_create_playlist(plex, MY_PLAYLIST)
    if not existing_playlist:
        return

    show_weighted_episodes = get_unwatched_episodes(plex, LIBRARY_NAME, COLLECTION_NAME)
    if NUMBER_OF_EP_OVERRIDE <= 0:
        NUMBER_OF_EP_OVERRIDE = len(show_weighted_episodes)

    final_playlist = weighted_show_selection(show_weighted_episodes, NUMBER_OF_EP_OVERRIDE)
    if final_playlist:
        logging.info(f'Updating {len(final_playlist)} shows to playlist.')
        update_playlist(existing_playlist, final_playlist)
    else:
        logging.info("No unwatched episodes available to add to the playlist.")

if __name__ == "__main__":
    main()
