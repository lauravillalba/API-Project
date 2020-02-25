import os
from dotenv import load_dotenv
load_dotenv()

# Connect to the database

LOCAL_DB=os.getenv('LOCAL_DB')
PORT=os.getenv('PORT')