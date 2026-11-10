import os
from pathlib import Path

from swingmusic.settings import Paths
from swingmusic.config import UserConfig


def is_path_within_root_dirs(filepath: str) -> bool:
    """
    Check if a filepath is within one of the configured root directories.
    Prevents directory traversal attacks.
    """
    config = UserConfig()
    resolved_path = Path(filepath).resolve()

    for root_dir in config.rootDirs:
        if root_dir == "$home":
            root_path = Path.home().resolve()
        else:
            root_path = Path(root_dir).resolve()

        # Check if resolved_path is the root or a child of root
        if resolved_path == root_path or root_path in resolved_path.parents:
            return True

    return False


def dirs_toward_root_dirs(dirpath: str) -> list[str]:
    """
    The folders right below a path that sits above root directories: each
    root directory or the folder leading to it.
    """
    path = Path(dirpath).resolve()
    children: list[str] = []

    for root_dir in UserConfig().rootDirs:
        root_path = Path.home().resolve() if root_dir == "$home" else Path(root_dir).resolve()

        if path in root_path.parents:
            child = (path / root_path.relative_to(path).parts[0]).as_posix()
            if child not in children:
                children.append(child)

    return children


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
