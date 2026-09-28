"""Cloud Run entrypoint that stores game data on a mounted volume."""
import os

import storage
from app import app

data_directory = os.environ.get("GAME_DATA_DIR", os.path.dirname(storage.DATA_FILE))
storage.DATA_FILE = os.path.join(data_directory, "data.json")