from pathlib import Path

from dotenv import load_dotenv

from artref.core.utils import require_env

load_dotenv()
UNSPLASH_KEY = require_env("UNSPLASH_KEY")

SCRYFALL_URL = "https://api.scryfall.com"
UNSPLASH_URL = "https://api.unsplash.com"
WALLHAVEN_URL = "https://wallhaven.cc/api/v1"

CACHE_DIR = Path.home() / ".cache" / "artref"
CACHE_EXPIRE = 7 * 24 * 60 * 60  # 7 days

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 8000

COUNT_DEFAULT = 3
COUNT_MIN = 1
COUNT_MAX = 10

FILENAME_LOG = "artref.json"
