"""
Configuration module for the FastAPI application.

This module defines global configuration settings that are used throughout the application. It includes
settings for network parameters such as the server's host address and port, along with any other
environment-specific settings that need to be centrally managed.

The configuration settings can be easily adjusted to accommodate different deployment environments,
such as development, testing, and production.

Attributes:
    SERVER_HOST (str): The hostname where the FastAPI server will run. Default is '127.0.0.1'.
    SERVER_PORT (int): The port on which the FastAPI server will listen. Default is 8000.

Example:
    Accessing configuration settings:
        from config import SERVER_HOST, SERVER_PORT

        def run_server():
            uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT)

This approach centralizes configuration management, making the application easier to configure and deploy.

"""

__author__ = "Utkarsh Raj"
__version__ = "1.0.0"


# Define server settings
SERVER_HOST = "0.0.0.0"  # Make 0.0.0.0 to allow access from other devices
SERVER_PORT = 8000  # Default port for Uvicorn
