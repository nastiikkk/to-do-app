import os

from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
allow_origin = os.getenv("CORS_ALLOW_ORIGIN")
