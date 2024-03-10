import re

from app.utils.filesystem import get_path_depth
from app.store.tracks import TrackStore
 
def parse_tracks(m3u_file_string):
    """
    Parses m3u files for tracks.
    Takes in raw m3u file string as a parameter.
    """

    tracks = []
    for line in m3u_file_string.split("\n#EXTINF:"):
        
        if "#EXTM3U" in line:
            continue

        default_patterns = [
            r'(?P<duration>\d+),(?P<artist>.+?) - (?P<title>.+)\n(?P<file_path>.+)',
            r'(?P<duration>\d+),(?P<artist>.+?) - (?P<title>.+)', 
            ]
        
        for pattern in default_patterns:
            match =  re.match(pattern, line)

            if not match:
                continue

            track = {}

            try:
                track['duration'] = match.group('duration')
                track['artist'] = match.group('artist')
                track['title'] = match.group('title')
            except: 
                continue

            try:
                track['file_path'] = match.group('file_path')
            except: 
                pass

            track['file_exists'] = False
            tracks.append(track)
            break

    return tracks if tracks else None


def filter_by_path(track):
    if 'file_path' not in track.keys():
        return []
    file_path = track['file_path']

    # Check if there are any tracks with exact path, if duration matches, skip artist matching
    store_results = TrackStore.get_tracks_by_filepaths(get_path_depth(file_path, False)[:-1])
    if len(store_results) == 1 and abs(int(track['duration']) - int(store_results[0].duration)) <= 5:
        return store_results[0]

    store_results = TrackStore.get_tracks_containing_filepaths(get_path_depth(file_path))
    return store_results


def match_track(track):
    """
    Takes in the track following the structure in the parse_tracks function.
    """

    filtered_results = []
    
    path_filtered = filter_by_path(track)
    if type(path_filtered) != list:
        return path_filtered
    
    filtered_results.extend(path_filtered)
    filtered_results.extend(TrackStore.get_tracks_by_trackname(track['title']))

    for result in filtered_results:
        artists = track['artist'].split(';')
        
        for _artist in artists:
            if _artist.lower() in [artist.name.lower() for artist in result.artists]:                
                if abs(int(track['duration']) - int(result.duration)) <= 5:
                    return result
    
    # Some other patterns that can be added in the future
    return None
