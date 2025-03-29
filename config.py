from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")  # Get API key securely

if not AIPROXY_TOKEN:
    raise ValueError("⚠️ AIPROXY_TOKEN is not set in .env file!")
