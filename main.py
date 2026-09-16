from subprocess import CalledProcessError
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from vmaf import vmaf_compare

MAX_FILE_SIZE = 250 * 1024 * 1024  # File limit: 250 MB in bytes

app = FastAPI()  # Initialize the FastAPI application


@app.get("/")  # Define a GET endpoint for the root URL

def home():  # Define the root endpoint function
    return {"message": "VMAF API is running"}  # Return a JSON response indicating that the API is running


@app.post("/vmaf")  # Define a POST endpoint for computing VMAF


def calculate_vmaf(reference: UploadFile = File(...), distorted: UploadFile = File(...)) -> dict:  # Define the endpoint function to compute VMAF
    """
    This endpoint computes the VMAF score between a reference video and a distorted video uploaded by the user.
    It uses the vmaf_compare function to perform the computation.
    Parameters:
    - reference: The reference video file uploaded by the user.
    - distorted: The distorted video file uploaded by the user.
    Returns:
    - A dictionary containing the computed VMAF score.
    """

    print(">>> FUNCTION 'calculate_vmaf' EXECUTED <<<", flush=True)  # Print a message indicating that the VMAF calculation has started

    if not reference.filename or not distorted.filename:  # Error handling #1: check if both video files are provided
        raise HTTPException(
            status_code=400,
            detail="Invalid input: both video files must be provided"
        )

    reference.file.seek(0, 2)  # Move the file pointer to the end of the reference video file to determine its size
    reference_size = reference.file.tell()  # Get the size of the reference video file

    distorted.file.seek(0, 2)  # Move the file pointer to the end of the distorted video file to determine its size
    distorted_size = distorted.file.tell()  # Get the size of the distorted video file

    if reference_size > MAX_FILE_SIZE or distorted_size > MAX_FILE_SIZE:  # Error handling #3: check if either video file exceeds the maximum allowed size
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB"
        )


    print("REFERENCE SIZE:", reference_size, flush=True)  # Print the size of the reference video file for debugging purposes
    print("DISTORTED SIZE:", distorted_size, flush=True)  # Print the size of the distorted video file for debugging purposes

    reference.file.seek(0)  # Move the file pointer back to the beginning of the reference video file for reading
    distorted.file.seek(0)  # Move the file pointer back to the beginning of the distorted video file for reading

    if reference_size == 0 or distorted_size == 0:  # Error handling #2: check if both video files contain data
        raise HTTPException(
            status_code=400,
            detail="Both video files must contain data"
        )
  

    with tempfile.NamedTemporaryFile(suffix=".mp4") as ref_file:
        shutil.copyfileobj(reference.file, ref_file)
        #ref_file.write(reference.file.read())  # Write the contents of the uploaded reference video file to a temporary file
        ref_file.flush()  # Flush the temporary file to ensure all data is written before proceeding

        with tempfile.NamedTemporaryFile(suffix=".mp4") as dist_file:
            shutil.copyfileobj(distorted.file, dist_file)
            #dist_file.write(distorted.file.read())  # Write the contents of the uploaded distorted video file to a temporary file
            dist_file.flush()  # Flush the temporary file to ensure all data is written before proceeding

            try:
                result = vmaf_compare(ref_file.name, dist_file.name)
            except CalledProcessError:  # Error handling #4: catch CalledProcessError raised by subprocess.run() in vmaf_compare() if FFmpeg fails to execute properly
                raise HTTPException(
                    status_code=400,
                    detail="Invalid video file"
                )
            except RuntimeError as e:  # Error handling #5: catch RuntimeError raised by vmaf_compare() if VMAF computation exceeds the timeout limit
                raise HTTPException(
                    status_code=504,
                    detail=str(e)
                )


    return {"vmaf": result}
