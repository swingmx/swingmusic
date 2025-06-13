from swingmusic.utils.threading import background


import subprocess


@background
def start_transcoding(
    input_path: str, output_path: str, bitrate: str, container_args: list[str], compression_level: int = 12
):
    """
    Starts a background transcoding process for an audio file.

    This function uses FFmpeg to transcode an audio file from one format to another,
    with specified bitrate and container format. It runs as a background task.

    Args:
        input_path (str): The path to the input audio file.
        output_path (str): The path where the transcoded file will be saved.
        bitrate (str): The desired bitrate for the output file (e.g., "128k").
        container_args (list[str]): FFmpeg arguments specific to the output container format.
        compression_level (int): Compression level (0-9, default: 6).

    Returns:
        None

    Note:
        This function is decorated with @background, which means it runs asynchronously.
        The actual transcoding process is handled by FFmpeg in a subprocess.
        The function will print status messages about the transcoding process.
    """
    # Base command
    command = [
        "ffmpeg",
        "-i",
        input_path,
        "-map_metadata", "0",  # Add this line to copy metadata
        "-b:a",
        bitrate,
        "-vn",
        "-compression_level",
        str(compression_level),
        # REVIEW: Idk what any flag below this point does!
        "-movflags",
        "faststart+frag_keyframe+empty_moov",
        "-write_xing",
        "0",
        "-fflags",
        "+bitexact",
    ]

    # Add format-specific parameters
    command.extend(container_args)

    # Add output path and overwrite flag
    command.extend([output_path, "-y"])

    process = subprocess.Popen(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    print(f"Started transcoding process with PID: {process.pid}")

    try:
        # Wait for the process to complete
        process.wait()
        print(f"Transcoding process (PID: {process.pid}) completed")
    except KeyboardInterrupt:
        print(f"Transcoding interrupted. Terminating process (PID: {process.pid})")
    finally:
        # Ensure the process is terminated
        try:
            process.terminate()
            process.wait(timeout=5)  # Wait up to 5 seconds for graceful termination
        except subprocess.TimeoutExpired:
            print(
                f"Process (PID: {process.pid}) did not terminate gracefully. Killing..."
            )
            process.kill()