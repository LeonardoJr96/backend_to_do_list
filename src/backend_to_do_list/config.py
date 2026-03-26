import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def validation():

    missing = []

    if not DATABASE_URL:
        missing.append("DATABASE_URL")
    
    if missing:
        raise ValueError(f"Missing or invalid required environment variables: {', '.join(missing)}")