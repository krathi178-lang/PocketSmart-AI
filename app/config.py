from pathlib import Path
import os
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/'.env')
APP_NAME=os.getenv('APP_NAME','PocketSmart AI')
SECRET_KEY=os.getenv('SECRET_KEY','dev-only-change-me')
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY','').strip()
GEMINI_MODEL=os.getenv('GEMINI_MODEL','gemini-2.5-flash')
COOKIE_SECURE=os.getenv('COOKIE_SECURE','false').lower()=='true'
DATA_DIR=BASE_DIR/'data'; DATA_DIR.mkdir(exist_ok=True)
SESSION_COOKIE='pocketsmart_token'; JWT_ALGORITHM='HS256'
