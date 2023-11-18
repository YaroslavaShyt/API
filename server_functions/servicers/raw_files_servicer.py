from utils.imports import raw_files_pb2_grpc, sessionmaker, raw_files_pb2, or_
from database.engine import engine
from database.tables import raw_files

Session = sessionmaker(bind=engine)


class RawFilesServicer(raw_files_pb2_grpc.RawFilesServiceServicer):
    def CreateRecordRawFiles(self, request, context):
      #  try:
        with Session() as session:
            new_record = raw_files.insert().values(
                projectid=request.project_id, data=request.data, status=request.status)
            session.execute(new_record)
            session.commit()
            session.close()
        result = {"success": True, "message": "Record created"}
   # except Exception:
   #     result = {"success": False, "message": Exception}
        return raw_files_pb2.CreateResponseRawFiles(**result)

    def ReadRecordRawFiles(self, request, context):
        try:
            with Session() as session:
                conditions = []
                if request.id:
                    conditions.append(raw_files.c.id == request.id)
                if request.name:
                    conditions.append(raw_files.c.name == request.name)
                if request.description:
                    conditions.append(
                        raw_files.c.description == request.description)
                if request.status:
                    conditions.append(raw_files.c.status == request.status)

                if conditions:
                    record = raw_files.select().where(or_(*conditions))
             #   else:
             #       record = projects.select()
                result = session.execute(record).fetchone()
                session.close()

                if result:
                    data = {
                        "success": True,
                        "id": result[0],
                        "name": result[1],
                        "description": result[2],
                        "timestamp": str(result[3]),
                        "status": result[4]}
                else:
                    data = {"success": False, "message": "No results"}
        except Exception as ex:
            data = {"success": False, "message": str(ex)}
        return raw_files_pb2.ReadResponseRawFiles(**data)

    def UpdateRecordRawFiles(self, request, context):
        try:
            with Session() as session:

                conditions = []
                if request.id:
                    conditions.append(raw_files.c.id == request.id)
                if request.name:
                    conditions.append(raw_files.c.name == request.name)
                if request.description:
                    conditions.append(raw_files.c.description ==
                                      request.description)
                if request.status:
                    conditions.append(raw_files.c.status == request.status)

                if conditions:
                    update_data = {}

                    if request.name:
                        update_data["name"] = request.name
                    if request.description:
                        update_data["description"] = request.description

                    if update_data:
                        update_query = raw_files.update().where(or_(*conditions)).values(
                            **update_data
                        )
                        session.execute(update_query)
                        session.commit()
                        session.close()
                        result = {"success": True, "message": "Record updated"}
                    else:
                        result = {"success": False,
                                  "message": "No parameters to update."}
                else:
                    result = {"success": False,
                              "message": "No parameters. Provide at least an id."}
        except Exception as ex:
            result = {"success": False, "message": str(ex)}
        return raw_files_pb2.UpdateResponseRawFiles(**result)

    def DeleteRecordRawFiles(self, request, context):
        try:
            with Session() as session:

                conditions = []
                if request.id:
                    conditions.append(raw_files.c.id == request.id)
                if request.name:
                    conditions.append(raw_files.c.name == request.name)
                if request.description:
                    conditions.append(
                        raw_files.c.description == request.description)
                if request.status:
                    conditions.append(raw_files.c.status == request.status)

                if conditions:
                    delete_query = raw_files.delete().where(
                        or_(*conditions))
                    message = "Record deleted."
                else:
                    delete_query = raw_files.delete()
                    message = "Records deleted."
                session.execute(delete_query)
                session.commit()
                session.close()
                result = {"success": True, "message": message}
        except Exception as ex:
            result = {"success": False, "message": str(ex)}
        return raw_files_pb2.UpdateResponseRawFiles(**result)
