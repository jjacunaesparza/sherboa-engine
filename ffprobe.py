from subprocess import CalledProcessError, run


def is_valid_video(file_path: str) -> bool:
    """
    Checks whether a file contains a valid video stream.
    Parameters:
    - file_path: Path to the video file to be checked.
    Returns:
    - True if the file is a valid video, False otherwise.
    """
    try:
        run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=codec_type",
                "-of", "csv=p=0", file_path
             ],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except CalledProcessError:
        return False