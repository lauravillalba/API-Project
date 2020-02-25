import os
import dotenv
from pathlib import Path  # python3 only
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(env_path)
dotenv.load_dotenv(dotenv_path=env_path)


# Connect to the database
dbURL = "mongodb+srv://admin:admin@cluster0-xtczl.mongodb.net/api_db?retryWrites=true&w=majority"
if not dbURL:
    raise ValueError("You should specify MONGODB_URL environment variable")