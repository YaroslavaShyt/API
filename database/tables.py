from utils.imports import Table, Column, Integer, String, TIMESTAMP, MetaData, func

metadata = MetaData()

projects = Table('projects', metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('name', String(255)),
                 Column('description', String(255)),
                 Column('timestamp', TIMESTAMP, server_default=func.now()),
                 Column('status', String(255))
                 )