from database.connection_params import *
from utils.imports import create_engine

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}", echo=True)
