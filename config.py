# -*- coding: utf-8 -*-

"""
Configuration file for SciHub Web Application
"""

import os

# Flask Configuration
DEBUG = False
HOST = '0.0.0.0'
PORT = 5000

# File Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'downloads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf'}

# SciHub Configuration
MAX_SEARCH_RESULTS = 50
DEFAULT_SEARCH_RESULTS = 10
SEARCH_TIMEOUT = 30

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Create downloads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
