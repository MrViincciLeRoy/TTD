# TTD Project
## Overview
The TTD project is a Python-based tool that automates the process of uploading videos to YouTube using the Google API.
## Key Features
- Uploads videos to YouTube
- Automatically generates video titles and descriptions
- Supports resumable uploads
## Tech Stack
- Python 3.x
- Google API Client Library
- pickle for token storage
## Installation
To install the required dependencies, run the following command: `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib`
## Usage
1. Create a project in the Google Cloud Console and enable the YouTube Data API v3
2. Create credentials for your project and download the JSON key file
3. Run the script and follow the authentication prompts
## Environment Variables
- TOKEN_PATH: path to the token storage file
- VIDEO_PATH: path to the video file to upload
## Code
```
import json
import os
import pickle
import sys
from datetime import datetime
...
```
## Notes
- Make sure to replace the VIDEO_PATH and TOKEN_PATH variables with your own values
- This project uses the pickle library to store tokens, make sure to handle them securely