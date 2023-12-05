from utils.imports import Table, Column, Integer, String, MetaData, func, DATETIME, ForeignKey, BINARY

metadata = MetaData()

projects = Table('v_Projects', metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('name', String(255)),
                 Column('description', String(255)),
                 Column('timestamp', DATETIME, server_default=func.now()),
                 Column('status', Integer)
                 )

users = Table('v_Users', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('name', String(30)),
              Column('username', String(30)),
              Column('key', BINARY(16)),
              Column('hash', BINARY),
              Column('salt', String(100)),
              Column('status', Integer),
              Column('description', String(200), default='No information'),
              Column('timestamp', DATETIME)
              )

project_members = Table('v_ProjectMembers', metadata,
                        Column('id', Integer, primary_key=True,
                               autoincrement=True),
                        Column('projectid', Integer,
                               ForeignKey("projects.id")),
                        Column('userid', Integer, ForeignKey("users.id")),
                        Column('permissionid', Integer,
                               ForeignKey("memberPermissions.id")),
                        )

anomalies = Table('v_Anomalies', metadata,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('projectid', Integer, ForeignKey("projects.id")),
                  Column('data', BINARY),
                  Column('timestamp', DATETIME),
                  Column('status', Integer),
                  Column('name', String(30)),
                  Column('tags', String(50)),
                  Column('description', String(200), default='No information'),
                  Column('radius', Integer),
                  Column('scale', Integer),
                  Column('processedByMemberId', Integer,
                         ForeignKey('projectMembers.id'))
                  )


files = Table('v_Rawfiles', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('projectid', Integer, ForeignKey("projects.id")),
              Column('data', BINARY),
              Column('timestamp', DATETIME),
              Column('status', Integer),
              Column('description', String(200), default='No information'),
              Column('processedByMemberId', Integer,
                     ForeignKey("projectMembers.id"))
              )


links = Table('v_Links', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('projectId', Integer, ForeignKey('projects.id')),
              Column('token', String(256)),
              Column('expires', DATETIME),
              Column('status', String(255))
              )
