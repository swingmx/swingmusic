"""
This module contains larger functions for the server
"""

import time
from progress.bar import Bar
import requests
import os
from mutagen.flac import MutagenError
from app import helpers
from app import instances
from app import api

def populate():
    '''
    Populate the database with all songs in the music directory

    checks if the song is in the database, if not, it adds it
    also checks if the album art exists in the image path, if not tries to
    extract it.
    '''
    print('\nchecking for new tracks')
    files = helpers.run_fast_scandir(helpers.home_dir, [".flac", ".mp3"])[1]

    for file in files:
        file_in_db_obj = instances.songs_instance.find_song_by_path(file)

        try:
            image = file_in_db_obj['image']

            if not os.path.exists(os.path.join(helpers.app_dir, 'images', 'thumbnails', image)):
                helpers.extract_thumb(file)
        except:
            image = None

        if image is None:
            try:
                helpers.getTags(file)
            except MutagenError:
                pass
    api.all_the_f_music = helpers.getAllSongs()
    print('\ncheck done')


def populate_images():
    all_songs = instances.songs_instance.get_all_songs()

    artists = []

    for song in all_songs:
        this_artists = song['artists'].split(', ')

        for artist in this_artists:
            if artist not in artists:
                artists.append(artist)

    bar = Bar('Processing images', max=len(artists))
    for artist in artists:
        file_path = helpers.app_dir + '/images/artists/' + \
            artist.replace('/', '::') + '.jpg'

        if not os.path.exists(file_path):
            url = 'https://api.deezer.com/search/artist?q={}'.format(artist)

            try:
                response = requests.get(url)
            except:
                print('\n sleeping for 5 seconds')
                time.sleep(5)
                response = requests.get(url)

            data = response.json()

            try:
                img_data = data['data'][0]['picture_xl']
            except:
                img_data = None

            if img_data is not None:
                helpers.save_image(img_data, file_path)

        bar.next()

    bar.finish()
