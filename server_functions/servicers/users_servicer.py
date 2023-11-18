from utils.imports import sessionmaker, or_, users_pb2_grpc, users_pb2
from database.engine import engine
from database.tables import users

Session = sessionmaker(bind=engine)


class UsersServicer(users_pb2_grpc.UserServiceServicer):
    def CreateUsersRecord(self, request, context):
        error_messages = []
        try:
            with Session() as session:

                # check <Name>
                if not request.name or not request.name.strip():
                    error_messages.append(
                        'Error: <Name> cannot be empty or include whitespaces only.')

                # check <Username>
                if not request.username or not request.username.strip():
                    error_messages.append(
                        'Error: <Username> cannot be empty or include whitespaces only.')

                # check <Key>
                if not request.key:
                    error_messages.append(
                        'Error: <Key> cannot be empty.')

                # check <Hash>
                if not request.hash:
                    error_messages.append(
                        'Error: <Hash> cannot be empty.')

                # check <Status>
                if request.status not in (0, 1):
                    error_messages.append(
                        f'Error: <Status> cannot be "{request.status}". Only allowed values - 0 or 1')

                 # if errors - do not do database query
                if error_messages:
                    result = {"success": False, "message": error_messages}
                else:
                    new_record = users.insert().values(
                        name=request.name,
                        username=request.username,
                        key=request.key,
                        hash=request.hash,
                        salt=request.salt if request.salt else None,
                        status=request.status,
                        description=request.description if request.description else None,
                    )
                    session.execute(new_record)
                    session.commit()
                    result = {"success": True,
                              "message": "USERS: Record created"}
        except Exception as ex:
            result = {"success": False, "message": str(ex)}
        return users_pb2.CreateUsersResponse(**result)

    def ReadUsersRecord(self, request, context):
        try:
            with Session() as session:
                conditions = []
                if request.id:
                    conditions.append(users.c.id.in_(request.id))
                if request.name:
                    conditions.append(users.c.name.in_(request.name))
                if request.key:
                    conditions.append(users.c.key.in_(request.key))
                if request.hash:
                    conditions.append(users.c.hash.in_(request.hash))
                if request.salt:
                    conditions.append(users.c.salt.in_(request.hash))
                if request.status:
                    conditions.append(users.c.status.in_(request.status))
                if request.description:
                    conditions.append(
                        users.c.description.in_(request.description))
                if request.timestamp:
                    conditions.append(users.c.timestamp.in_(request.timestamp))

                if not conditions:
                    # If no conditions - fetch all records
                    results = session.query(users).all()
                else:
                    # If conditions - filter the records
                    results = session.query(users).filter(
                        or_(*conditions)).all()

                if results:
                    data = {
                        "success": True,
                        "data": [{
                            "id": result.id,
                            "name": result.name,
                            "key": result.key,
                            "hash": result.hash,
                            "salt": result.salt,
                            "status": result.status,
                            "description": result.description,
                            "timestamp": str(result.timestamp)} for result in results]
                    }
                else:
                    data = {"success": False, "message": "USERS: No results"}
        except Exception as ex:
            data = {"success": False, "message": str(ex)}
        return users_pb2.ReadUsersResponse(**data)

    def UpdateUsersRecord(self, request, context):
        try:
            with Session() as session:

                conditions = []
                if request.id:
                    conditions.append(users.c.id.in_(request.id))
                if request.name:
                    conditions.append(users.c.name.in_(request.name))
                if request.key:
                    conditions.append(users.c.key.in_(request.key))
                if request.hash:
                    conditions.append(users.c.hash.in_(request.hash))
                if request.salt:
                    conditions.append(users.c.salt.in_(request.hash))
                if request.status:
                    conditions.append(users.c.status.in_(request.status))
                if request.description:
                    conditions.append(
                        users.c.description.in_(request.description))
                if request.timestamp:
                    conditions.append(users.c.timestamp.in_(request.timestamp))

                if not session.query(users).filter(or_(*conditions)).count():
                    return users_pb2.UpdateUsersResponse(success=False, message="No matching records found.")

                if conditions:
                    update_data = {
                        "name": request.update_data.name if request.update_data.name else None,
                        "username": request.update_data.username if request.update_data.username else None,
                        "key": request.update_data.key if request.update_data.key else None,
                        "hash": request.update_data.hash if request.update_data.hash else None,
                        "salt": request.update_data.salt if request.update_data.salt else None,
                        "status": request.update_data.status if request.update_data.status else None,
                        "description": request.update_data.description if request.update_data.description else None,
                    }

                    if any(update_data.values()):
                        update_query = users.update().where(or_(*conditions)).values(
                            **{k: v for k, v in update_data.items() if v is not None}
                        )
                        session.execute(update_query)
                        session.commit()
                        result = {"success": True, "message": "Record updated"}

                    else:
                        result = {"success": False,
                                  "message": "No parameters to update."}
                else:
                    result = {"success": False,
                              "message": "No parameters. Provide at least an id."}
        except Exception as ex:
            result = {"success": False, "message": str(ex)}
        return users_pb2.UpdateUsersResponse(**result)

    def DeleteUsersRecord(self, request, context):
        try:
            with Session() as session:

                conditions = []
                if request.id:
                    conditions.append(users.c.id.in_(request.id))
                if request.name:
                    conditions.append(users.c.name.in_(request.name))
                if request.key:
                    conditions.append(users.c.key.in_(request.key))
                if request.hash:
                    conditions.append(users.c.hash.in_(request.hash))
                if request.salt:
                    conditions.append(users.c.salt.in_(request.hash))
                if request.status:
                    conditions.append(users.c.status.in_(request.status))
                if request.description:
                    conditions.append(
                        users.c.description.in_(request.description))
                if request.timestamp:
                    conditions.append(users.c.timestamp.in_(request.timestamp))

                if not session.query(users).filter(or_(*conditions)).count():
                    return users_pb2.DeleteUsersResponse(success=False, message="No matching records found.")

                if conditions:
                    delete_query = users.delete().where(or_(*conditions))
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
        return users_pb2.UpdateUsersResponse(**result)
