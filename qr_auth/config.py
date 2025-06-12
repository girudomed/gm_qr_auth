from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
BRANCH_ID = os.getenv('BRANCH_ID', '1')
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecret')
