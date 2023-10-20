from utils.imports import os, load_dotenv

load_dotenv()

host = os.getenv("HOST")
port = int(os.getenv("PORT"))
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
server_port = os.getenv("SERVER_PORT")
