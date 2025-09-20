import os
from pathlib import Path
from swingmusic.settings import Paths


def get_client_files_extensions():
    """
    Get all the file extensions for the client files
    """

    extensions = set()
    for root, dirs, files in os.walk(Paths().client_path):
        for file in files:
            ext = file.split(".")[-1]
            extensions.add("." + ext)

    return extensions


def normalize_paths(paths: list[str]) -> list[str]:
    """
    Given a list of paths, returns a list of paths where no path is a child of another path
    """
    if not paths:
        return []

    # Convert to absolute paths for proper comparison
    abs_paths = [Path(path).resolve() for path in paths]

    # Sort paths by length (shorter paths first) to check parents before children
    sorted_paths = sorted(abs_paths, key=lambda p: len(p.parts))

    normalized = []

    for current_path in sorted_paths:
        # Check if current_path is a child of any path already in normalized list
        is_child = False
        for existing_path in normalized:
            try:
                # Check if current_path is relative to existing_path
                current_path.relative_to(existing_path)
                is_child = True
                break
            except ValueError:
                # current_path is not relative to existing_path, continue checking
                continue

        # Only add if it's not a child of any existing path
        if not is_child:
            normalized.append(current_path.as_posix())

    return normalized
