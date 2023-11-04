from utils.imports import sessionmaker, or_, users_pb2_grpc, users_pb2
from database.engine import engine
from database.tables import users

Session = sessionmaker(bind=engine)


class UsersServicer(users_pb2_grpc.UserServiceServicer):
    def CreateRecordUsers(self, request, context):
       # try:
        with Session() as session:
            print(request)
            new_record = users.insert().values(
                name=request.name,
                key=request.key,
                hash=request.hash,
                salt=request.salt,
                status=request.status,
                description=request.description,
            )
            session.execute(new_record)
            session.commit()
            session.close()
        result = {"success": True, "message": "USERS: Record created"}
  #  except Exception as ex:
  #      result = {"success": False, "message": str(ex)}
        return users_pb2.CreateResponseUsers(**result)

    def ReadRecordUsers(self, request, context):
        try:
            with Session() as session:
                conditions = []
                if request.id:
                    conditions.append(users.c.id == request.id)
                if request.name:
                    conditions.append(users.c.name == request.name)
                if request.key:
                    conditions.append(users.c.key == request.key)
                if request.hash:
                    conditions.append(users.c.hash == request.hash)
                if request.salt:
                    conditions.append(users.c.salt == request.hash)
                if request.status:
                    conditions.append(users.c.status == request.status)
                if request.description:
                    conditions.append(
                        users.c.description == request.description)
                if request.timestamp:
                    conditions.append(users.c.timestamp == request.timestamp)

                if conditions:
                    record = users.select().where(or_(*conditions))
            #    else:
            #        record = users.select()
                result = session.execute(record).fetchone()
                session.close()

                if result:
                    data = {
                        "success": True,
                        "name": result[1],
                        "key": result[2],
                        "hash": result[3],
                        "salt": result[4],
                        "status": result[5],
                        "description": result[6],
                        "timestamp": str(result[7]),
                    }
                else:
                    data = {"success": False, "message": "USERS: No results"}
        except Exception as ex:
            data = {"success": False, "message": str(ex)}
        return users_pb2.ReadResponseUsers(**data)

    def UpdateRecordUsers(self, request, context):
        try:
            with Session() as session:

                conditions = []
                if request.id:
                    conditions.append(users.c.id == request.id)

                if conditions:
                    update_data = {}

                    if request.name:
                        update_data["name"] = request.name
                    if request.description:
                        update_data["description"] = request.description
                    if request.key:
                        update_data["key"] = request.key
                    if request.hash:
                        update_data["hash"] = request.hash
                    if request.salt:
                        update_data["salt"] = request.salt
                    if request.status:
                        update_data["status"] = request.status
                    if request.description:
                        update_data["description"] = request.description

                    if update_data:
                        select_query = users.select().where(
                            or_(users.c.id == request.id))
                        data = session.execute(select_query).fetchone()
                        if data:
                            update_query = users.update().where(or_(*conditions)).values(
                                **update_data
                            )
                            session.execute(update_query)
                            session.commit()
                            session.close()
                            result = {"success": True,
                                      "message": "USERS: Record updated"}
                        else:
                            result = {"success": False,
                                      "message": "No records for this id."}
                    else:
                        result = {"success": False,
                                  "message": "No parameters to update."}
                else:
                    result = {"success": False,
                              "message": "No parameters. Provide at least an id."}
        except Exception as ex:
            result = {"success": False, "message": str(ex)}
        return users_pb2.UpdateResponseUsers(**result)

    def DeleteRecordUsers(self, request, context):
        try:
            with Session() as session:

                conditions = []
                if request.id:
                    conditions.append(users.c.id == request.id)
                if request.name:
                    conditions.append(users.c.name == request.name)
                if request.description:
                    conditions.append(
                        users.c.description == request.description)
                if request.status:
                    conditions.append(users.c.status == request.status)

                if conditions:
                    delete_query = users.delete().where(
                        or_(*conditions))
                    message = "Record deleted."
                else:
                    delete_query = users.delete()
                    message = "Records deleted."
                session.execute(delete_query)
                session.commit()
                session.close()
                result = {"success": True, "message": message}
        except Exception as ex:
            result = {"success": False, "message": str(ex)}
        return users_pb2.UpdateResponseUsers(**result)
