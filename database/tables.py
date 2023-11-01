from utils.imports import Table, Column, Integer, String, MetaData, func, DATETIME, ForeignKey

metadata = MetaData()

projects = Table('projects', metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('name', String(255)),
                 Column('description', String(255)),
                 Column('timestamp', DATETIME, server_default=func.now()),
                 Column('status', String(255))
                 )

links = Table('links', metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('projectid', Integer, ForeignKey('projects.id')),
                 Column('token', String(256)),
                 Column('expires', DATETIME),
                 Column('status', String(255))
                 )