from subprocess import CalledProcessError, run


# Function to validate input file
def is_valid_video(file_path: str) -> bool:
    """
    Checks whether a file contains a valid video stream.
    Parameters:
    - file_path: Path to the video file to be checked.
    Returns:
    - True if the file contains a video stream, False otherwise.
    """
    try:
        result = run(
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
        text_output = result.stdout.strip()  # Clean spaces and newlines

        if text_output == "video":  # Check if stream type is video
            return True
        else:
            return False
    except CalledProcessError:
        return False


# Function to validate video resolution
def get_video_dimensions(file_path: str) -> tuple[int, int]:
    """
    Returns the width and height of the first video stream.
    Parameters:
    - file_path: Path to the video file.
    Returns:
    - A tuple containing the video width and height.
    """
    result = run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=p=0:s=x", file_path
        ],
        check=True,
        capture_output=True,
        text=True
    )

    width, height = result.stdout.strip().split("x")
    return int(width), int(height)

