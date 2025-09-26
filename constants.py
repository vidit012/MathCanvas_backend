import os
from dotenv import load_dotenv
load_dotenv()

SERVER_URL = 'localhost'
PORT = '8900'
ENV = 'dev'

GEMINI_API_KEY =os.getenv("GEMINI_API_KEY")