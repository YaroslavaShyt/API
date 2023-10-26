from utils.imports import os, load_dotenv

load_dotenv()

#mysql params
#host = os.getenv("HOST")
#port = int(os.getenv("PORT"))
#user = os.getenv("USER")
#password = os.getenv("PASSWORD")
#database = os.getenv("DATABASE")

# server params
server_port = os.getenv("SERVER_PORT")

# ms sql params
database = os.getenv("DATABASE")
server = os.getenv("SERVER")
