from swingmusic.models.track import Track
from typing import List, Dict, Tuple
from collections import Counter


def violates_gap_rule(
    balanced_mix: Dict[int, Track], position: int, track: Track, gap: int = 3
) -> bool:
    """
    Check if placing the track at the given position violates the gap rule.

    The gap rule is violated if the track has an artist in common with any
    track within the gap range (default = 3).
    """
    track_artists = set(artist["artisthash"] for artist in track.artists)

    for i in range(max(0, position - gap), position):
        if i in balanced_mix:
            existing_artists = set(
                artist["artisthash"] for artist in balanced_mix[i].artists
            )
            if track_artists.intersection(existing_artists):
                return True

    return False


def find_next_position(
    balanced_mix: Dict[int, Track], start: int, track: Track, total_tracks: int
) -> int:
    """
    Find the next available position for the track, starting from 'start' and wrapping around.
    """
    for i in range(start, total_tracks):
        if i not in balanced_mix and not violates_gap_rule(balanced_mix, i, track):
            return i
    for i in range(start):
        if i not in balanced_mix and not violates_gap_rule(balanced_mix, i, track):
            return i
    return start  # If no better position is found, return the original position


def is_tracklist_balanced(tracks: List[Track], gap: int = 3) -> Tuple[bool, bool]:
    """
    Checks if a tracklist is balanced or can be balanced.

    Args:
    - tracks: List of Track objects
    - gap: Minimum number of tracks between songs by the same artist (default 3)

    Returns:
    - A tuple (can_be_balanced, is_currently_balanced)
    """
    total_tracks = len(tracks)

    # Count tracks per artist (considering only the first artist)
    artist_counts = Counter(track.artists[0]["artisthash"] for track in tracks)

    # Calculate the maximum number of tracks an artist can have in a balanced list
    max_tracks_per_artist = (total_tracks + gap) // (gap + 1)

    # Check if it's mathematically possible to balance the tracklist
    can_be_balanced = all(
        count <= max_tracks_per_artist for count in artist_counts.values()
    )

    if not can_be_balanced:
        return False, False

    # Check if the current arrangement is balanced
    is_currently_balanced = True
    artist_last_positions = {}

    for i, track in enumerate(tracks):
        artist = track.artists[0]["artisthash"]
        if artist in artist_last_positions:
            if i - artist_last_positions[artist] <= gap:
                is_currently_balanced = False
                break
        artist_last_positions[artist] = i

    return can_be_balanced, is_currently_balanced


def balance_mix(tracks: List[Track]) -> List[Track]:
    """
    Balances the mix by ensuring that the tracks in a mix are distributed evenly.
    Preserves the overall rating order of tracks while minimizing disruption.

    Tracks that need to be moved are moved down the tracklist until they no longer
    violate the gap rule.
    """
    can_be_balanced, is_balanced = is_tracklist_balanced(tracks)

    if is_balanced:
        # Already balanced, no need to modify
        return tracks

    # Proceed with best-effort balancing
    balanced_mix: Dict[int, Track] = {}
    total_tracks = len(tracks)

    for i, track in enumerate(tracks):
        if i in balanced_mix or not violates_gap_rule(balanced_mix, i, track):
            balanced_mix[i] = track
        else:
            new_position = find_next_position(balanced_mix, i, track, total_tracks)
            balanced_mix[new_position] = track

    # Convert the dictionary back to a list, preserving the new order
    return [balanced_mix[i] for i in sorted(balanced_mix.keys())]
