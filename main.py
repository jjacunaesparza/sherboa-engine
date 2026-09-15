import tempfile
from fastapi import FastAPI, UploadFile, File
from vmaf import vmaf_compare

app = FastAPI()  # Initialize the FastAPI application


@app.get("/")  # Define a GET endpoint for the root URL

def home():  # Define the root endpoint function
    return {"message": "VMAF API is running"}  # Return a JSON response indicating that the API is running


@app.post("/vmaf")  # Define a POST endpoint for computing VMAF


def calculate_vmaf(reference: UploadFile = File(...), distorted: UploadFile = File(...)) -> dict:  # Define the endpoint function to compute VMAF
    """"
    This endpoint computes the VMAF score between a reference video and a distorted video uploaded by the user.
    It uses the vmaf_compare function to perform the computation.
    Parameters:
    - reference: The reference video file uploaded by the user.
    - distorted: The distorted video file uploaded by the user.
    Returns:
    - A dictionary containing the computed VMAF score.
    """
    
    with tempfile.NamedTemporaryFile(suffix=".mp4") as ref_file:
        ref_file.write(reference.file.read())  # Write the contents of the uploaded reference video file to a temporary file
        ref_file.flush()  # Flush the temporary file to ensure all data is written before proceeding

        with tempfile.NamedTemporaryFile(suffix=".mp4") as dist_file:
            dist_file.write(distorted.file.read())  # Write the contents of the uploaded distorted video file to a temporary file
            dist_file.flush()  # Flush the temporary file to ensure all data is written before proceeding

            result = vmaf_compare(ref_file.name, dist_file.name)

    return {"vmaf": result}
