from database.connection_params import *
from utils.imports import create_engine

#ms sql
engine = create_engine(f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')


# mysql
# engine = create_engine(
#    f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')
