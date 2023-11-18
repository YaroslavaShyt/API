from datetime import datetime
from utils.imports import projects_pb2_grpc, sessionmaker, projects_pb2, or_
from database.engine import engine
from database.tables import projects

Session = sessionmaker(bind=engine)


class ProjectServicer(projects_pb2_grpc.ProjectsServiceServicer):
    def CreateRecordProjects(self, request, context):
        error_messages = []
        try:
            with Session() as session:
                # check <Name>
                if not request.name or not request.name.strip():
                    error_messages.append('Параметр <Name> не може бути порожнім або містити лише пробіли.')

                # check <Description>
                if not request.description or not request.description.strip():
                    error_messages.append(
                        'Параметр <Description> не може бути порожнім або містити лише пробіли.')
                    
                 # check <Status>
               # if not request.statue:
               #     error_messages.append(
               #         'Параметр <Status> не може бути порожнім або містити лише пробіли.')
                    
                # if errors - do not do database query
                if error_messages:
                    result = {"success": False, "messages": error_messages}
                else:
                    # if no messages - do database query
                    new_record = projects.insert().values(
                        name=request.name,
                        description=request.description,
                        status=request.status
                    )
                    session.execute(new_record)
                    session.commit()
                    result = {"success": True, "message": "Record created"}
        except Exception as e:
            result = {"success": False, "message": str(e)}
        return projects_pb2.CreateProjectsResponse(**result)

    def ReadRecordProjects(self, request, context):
        try:
            with Session() as session:
                conditions = []
                if request.id:
                    conditions.append(projects.c.id.in_(request.id))
                if request.name:
                    conditions.append(projects.c.name.in_(request.name))
                if request.description:
                    conditions.append(
                        projects.c.description.in_(request.description))
                if request.timestamp:
                    conditions.append(projects.c.timestamp.in_(
                        datetime.fromisoformat(request.timestamp)))
                if request.status:
                    conditions.append(projects.c.status.in_(request.status))

                if not conditions:
                    # If no conditions - fetch all records
                    results = session.query(projects).all()
                else:
                    # If conditions - filter the records
                    results = session.query(projects).filter(or_(*conditions)).all()

                if results:
                    data = {
                        "success": True,
                        "data": [{
                            "id": result.id,
                            "name": result.name,
                            "description": result.description,
                            "timestamp": str(result.timestamp),
                            "status": result.status,
                        } for result in results]
                    }
                else:
                    data = {"success": False, "message": "No results"}
        except Exception as ex:
            data = {"success": False, "message": str(ex)}
        return projects_pb2.ReadProjectsResponse(**data)
    

    def UpdateRecordProjects(self, request, context):
        try:
            with Session() as session:
                conditions = []

                if request.id:
                    conditions.append(projects.c.id.in_(request.id))
                if request.name:
                    conditions.append(projects.c.name.in_(request.name))
                if request.description:
                    conditions.append(
                        projects.c.description.in_(request.description))
                if request.timestamp:
                    conditions.append(projects.c.timestamp.in_(
                        datetime.fromisoformat(request.timestamp)))
                if request.status:
                    conditions.append(projects.c.status.in_(request.status))

    
                if not session.query(projects).filter(or_(*conditions)).count():
                    return projects_pb2.UpdateProjectsResponse(success=False, message="No matching records found.")

                update_data = {
                    "name": request.update_data.name if request.update_data.name else None,
                    "description": request.update_data.description if request.update_data.description else None,
                    "status": request.update_data.status if request.update_data.status else None,
                }

                if any(update_data.values()):
                    update_query = projects.update().where(or_(*conditions)).values(
                        **{k: v for k, v in update_data.items() if v is not None}
                    )
                    session.execute(update_query)
                    session.commit()
                    result = {"success": True, "message": "Record updated"}
                else:
                    result = {"success": False,
                            "message": "No parameters to update."}
        except Exception as ex:
            result = {"success": False, "message": str(ex)}

        return projects_pb2.UpdateProjectsResponse(**result)


    def DeleteRecordProjects(self, request, context):
        try:
            with Session() as session:
                conditions = []
                if request.id:
                    conditions.append(projects.c.id.in_(request.id))
                if request.name:
                    conditions.append(projects.c.name.in_(request.name))
                if request.description:
                    conditions.append(
                        projects.c.description.in_(request.description))
                if request.timestamp:
                    conditions.append(projects.c.timestamp.in_(
                        datetime.fromisoformat(request.timestamp)))
                if request.status:
                    conditions.append(projects.c.status.in_(request.status))

                
                if not session.query(projects).filter(or_(*conditions)).count():
                    return projects_pb2.DeleteProjectsResponse(success=False, message="No matching records found.")

                if conditions:
                    delete_query = projects.delete().where(or_(*conditions))
                    message = "Record deleted."
                else:
                    delete_query = projects.delete()
                    message = "Records deleted."
                session.execute(delete_query)
                session.commit()
                result = {"success": True, "message": message}
        except Exception as ex:
            result = {"success": False, "message": str(ex)}

        return projects_pb2.DeleteProjectsResponse(**result)


"""
error_messages = []
 # check <Name>
                if not request.name or not request.name.strip():
                    error_messages.append('Параметр <Name> не може бути порожнім або містити лише пробіли.')
                if not isinstance(request.name, str):
                    error_messages.append(f'Параметр <Name> має неочікуваний тип - {type(request.name)}. Очікувався - str(рядок)')

                # check <Description>
                if not request.description or not request.description.strip():
                    error_messages.append(
                        'Параметр <Description> не може бути порожнім або містити лише пробіли.')
                if not isinstance(request.description, str):
                    error_messages.append(f'Параметр <Description> має тип {type(request.description)}, очікувався - str(рядок).')

                # check <Status>
                if not request.description or not request.description.strip():
                    error_messages.append(
                        'Параметр <Status> не може бути порожнім або містити лише пробіли.')
                if not isinstance(request.status, int):
                    error_messages.append(f'Параметр <Status> має тип {type(request.status)}, очікувався - int(ціле число).')

                # if errors - do not do database query
                if error_messages:
                    result = {"success": False, "messages": error_messages}
                else:
                    # if no messages - do database query
"""
