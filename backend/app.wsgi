#!/usr/bin/env python3

import sys
import os



from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# Set the working directory to the directory of the WSGI script
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application  # Import your Flask app instance

#if __name__ == '__main__':
#  application.run()
