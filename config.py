__all__ = ['TOKEN', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_HOST', 'DB_PORT']

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
