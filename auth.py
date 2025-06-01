from dotenv import load_dotenv
import os

load_dotenv()

async def get_CLIENT_ID() -> str:
    return os.getenv("MAL_CLIENT_ID")