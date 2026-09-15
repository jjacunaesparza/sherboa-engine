import subprocess
import json
from pathlib import Path

FFMPEG = Path.home() / "projects" / "ffmpeg-vmaf" / "ffmpeg"

# Function to compute VMAF between reference and distorted videos
def vmaf_compare(reference, distorted) -> float:
    """
    Computes the VMAF score between a reference video and a distorted video using FFmpeg.
    Parameters:
    - reference: Path to the reference video file.
    - distorted: Path to the distorted video file.
    Returns:
    - score: The computed VMAF score rounded to two decimal places.
    """

    output = "vmaf.json"  # File to store the VMAF output in JSON format

    command = [  # Construct the FFmpeg command to compute VMAF
        str(FFMPEG),
        "-i", distorted,
        "-i", reference,
        "-lavfi", f"libvmaf=log_fmt=json:log_path={output}",
        "-f", "null",
        "-"
    ]
    
    subprocess.run(command, check=True)  # Run the FFmpeg command to compute VMAF and generate the JSON output

    with open(output, "r") as file:
        data = json.load(file)

    mean = data["pooled_metrics"]["vmaf"]["mean"]

    score = round(mean, 2)
    return score
