from utils.imports import projects_pb2_grpc, sessionmaker, projects_pb2, or_
from database.engine import engine
from database.tables import projects

Session = sessionmaker(bind=engine)


class ProjectServicer(projects_pb2_grpc.ProjectsServiceServicer):
    def CreateRecordProjects(self, request, context):
        try:
            with Session() as session:
                new_record = projects.insert().values(
                    name=request.name, description=request.description, status=request.status)
                session.execute(new_record)
                session.commit()
                session.close()
            result = {"success": True, "message": "Record created"}
        except Exception:
            result = {"success": False, "message": Exception}
        return projects_pb2.CreateResponseProjects(**result)

    def ReadRecordProjects(self, request, context):
        try:
            with Session() as session:
                conditions = []
                if request.id:
                    conditions.append(projects.c.id == request.id)
                if request.name:
                    conditions.append(projects.c.name == request.name)
                if request.description:
                    conditions.append(
                        projects.c.description == request.description)
                if request.status:
                    conditions.append(projects.c.status == request.status)

                if conditions:
                    record = projects.select().where(or_(*conditions))
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
        return projects_pb2.ReadResponseProjects(**data)

    def UpdateRecordProjects(self, request, context):
        try:
            with Session() as session:

                conditions = []
                if request.id:
                    conditions.append(projects.c.id == request.id)
                if request.name:
                    conditions.append(projects.c.name == request.name)
                if request.description:
                    conditions.append(projects.c.description ==
                                      request.description)
                if request.status:
                    conditions.append(projects.c.status == request.status)

                if conditions:
                    update_data = {}

                    if request.name:
                        update_data["name"] = request.name
                    if request.description:
                        update_data["description"] = request.description

                    if update_data:
                        update_query = projects.update().where(or_(*conditions)).values(
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
        return projects_pb2.UpdateResponseProjects(**result)

    def DeleteRecordProjects(self, request, context):
        try:
            with Session() as session:

                conditions = []
                if request.id:
                    conditions.append(projects.c.id == request.id)
                if request.name:
                    conditions.append(projects.c.name == request.name)
                if request.description:
                    conditions.append(
                        projects.c.description == request.description)
                if request.status:
                    conditions.append(projects.c.status == request.status)

                if conditions:
                    delete_query = projects.delete().where(
                        or_(*conditions))
                    message = "Record deleted."
                else:
                    delete_query = projects.delete()
                    message = "Records deleted."
                session.execute(delete_query)
                session.commit()
                session.close()
                result = {"success": True, "message": message}
        except Exception as ex:
            result = {"success": False, "message": str(ex)}
        return projects_pb2.UpdateResponseProjects(**result)
