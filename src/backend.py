"""
This module defines the FastAPI app and its routes for scheduling jobs. When run as a script, it starts a uvicorn server on port defined in the config.py file.

The app uses CORS middleware to handle cross-origin requests and defines endpoints to schedule jobs and retrieve job information. It interacts with the `algorithms` module
to calculate schedules based on different scheduling algorithms.

Endpoints:
- POST /schedule_jobs: Accepts JSON payload to schedule jobs based on application and platform data.
- GET /: Provides a basic test endpoint to confirm the app is running.

See the function docstrings within this module for more detailed API documentation.
"""

__author__ = "Utkarsh Raj"
__version__ = "1.0.0"


from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import jsonschema
from jsonschema import validate
import os

from config import SERVER_PORT, SERVER_HOST
import algorithms as alg


script_dir = os.path.dirname(__file__)
input_schema_file = os.path.join(script_dir, "input_schema.json")
output_schema_file = os.path.join(script_dir, "output_schema.json")

# Load the input and output schema
with open(input_schema_file) as f:
    input_schema = json.load(f)

with open(output_schema_file) as f:
    output_schema = json.load(f)

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://eslab2.pages.dev",
    "https://eslab.es.eti.uni-siegen.de"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/schedule_jobs")
def schedule_jobs(data: dict):
    """
    Schedule jobs based on the provided application and platform data.

    This endpoint processes a JSON payload containing application and platform configurations,
    then calculates schedules using Least Deadline First (LDF), Earliest Deadline First (EDF),
    Rate Monotonic (RMS) and Least Laxity (LL) scheduling algorithms
    on single-core setups.

    Args:
        data (dict): A dictionary containing 'application' and 'platform' data necessary for scheduling.

    Raises:
        HTTPException: If the 'application' or 'platform' data is missing or malformed, a 400 error is raised.

    Returns:
        dict: A dictionary containing schedules calculated using different algorithms:
              - schedule1: Schedule using Latest Deadline First (LDF) schedulin on single-core.
              - schedule2: Schedule using Earliest Deadline First (EDF) scheduling on single-core.
              - schedule3: Schedule using Rate Monotonic Scheduling (RMS) on single-core.
              - schedule4: Schedule using Least Laxity (LL) on single-core.
    """

    print("Received JSON data:", json.dumps(data, indent=4))

    # Validate the input as per input schema
    try:
        validate(instance=data, schema=input_schema)
        print("Input data is valid.")
    except jsonschema.exceptions.ValidationError as err:
        print("Input data is invalid:", err)
        raise HTTPException(400, "Invalid Input schema")

    application_data = data.get("application")
    platform_data = data.get("platform")

    ldf_single_node = alg.ldf_single_node(application_data)
    edf_single_node = alg.edf_single_node(application_data)
    ll_multinode = alg.ll_multinode(application_data, platform_data)
    ldf_multinode = alg.ldf_multinode(application_data, platform_data)
    edf_multinode = alg.edf_multinode(application_data, platform_data)

    response = {
        "schedule1": ldf_single_node,
        "schedule2": edf_single_node,
        "schedule3": ll_multinode,
        "schedule4": ldf_multinode,
        "schedule5": edf_multinode,
    }
    # Validate the schedules as per output schema
    try:
        for key, value in response.items():
            validate(instance=value, schema=output_schema)
            print(key, "Schedule is valid")
    except jsonschema.exceptions.ValidationError as err:
        print("Output data is not valid", err)
        raise HTTPException(500, "Invalid Output Schema")

    print(json.dumps(response, indent=4))
    return response


@app.get("/")
def read_root():
    """
    Retrieve the root URL. For testing purposes.

    Returns:
        dict: A simple dictionary with a greeting.
    """
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="info")
