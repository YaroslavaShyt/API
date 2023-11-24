from datetime import datetime
from utils.imports import anomalies_pb2_grpc, anomalies_pb2, sessionmaker, or_
from database.engine import engine
from database.tables import projects, anomalies

Session = sessionmaker(bind=engine)


class AnomaliesServicer(anomalies_pb2_grpc.AnomaliesServiceServicer):
    def CreateRecordAnomalies(self, request, context):
        error_messages = []
        try:
            with Session() as session:

                # check <ProjectId>
                conditions = [projects.c.id.in_(request.id)]
                if not session.query(projects).filter(or_(*conditions)).count():
                    return anomalies_pb2.CreateAnomaliesResponse(success=False, message=[f"No matching records found for projectId <{request.id}>"])

                # check <Name>
                if not request.name or not request.name.strip():
                    error_messages.append(
                        'Error: <Name> cannot be empty or include whitespaces only.')

                # check <Status>
                if request.status not in (0, 1):
                    error_messages.append(
                        f'Error: <Status> cannot be "{request.status}". Only allowed values - 0 or 1')

                # if errors - do not do database query
                if error_messages:
                    result = {"success": False, "message": error_messages}
                else:
                    # if no messages - do database query
                    new_record = anomalies.insert().values(
                        projectid=request.projectId,
                        data=request.data,
                        status=request.status,
                        name=request.name,
                        tags=request.tags,
                        description=request.description if (
                            request.description) else None,
                        radius=request.radius,
                        scale=request.scale,
                        processedByMemberId=request.processedByMemberId

                    )
                    session.execute(new_record)
                    session.commit()
                    result = {"success": True, "message": ["Record created"]}
        except Exception as e:
            result = {"success": False, "message": [str(e)]}
        return anomalies_pb2.CreateAnomaliesResponse(**result)

    def ReadRecordAnomalies(self, request, context):
        try:
            with Session() as session:
                conditions = []
                if request.id:
                    conditions.append(projects.c.id.in_(request.id))
                if request.projectId:
                    conditions.append(
                        projects.c.projectid.in_(request.projectid))
                if request.timestamp:
                    conditions.append(projects.c.timestamp.in_(
                        datetime.fromisoformat(request.timestamp)))
                if request.status:
                    conditions.append(projects.c.status.in_(request.status))
                if request.name:
                    conditions.append(projects.c.name.in_(request.name))
                if request.tags:
                    conditions.append(projects.c.tags.in_(request.tags))
                if request.description:
                    conditions.append(
                        projects.c.description.in_(request.description))
                if request.radius:
                    conditions.append(
                        projects.c.radius.in_(request.radius))
                if request.scale:
                    conditions.append(
                        projects.c.scale.in_(request.scale))
                if request.processedByMemberId:
                    conditions.append(
                        projects.c.processedByMemberId.in_(request.processedByMemberId))

                if not conditions:
                    # If no conditions - fetch all records
                    results = session.query(anomalies).all()
                else:
                    # If conditions - filter the records
                    results = session.query(anomalies).filter(
                        or_(*conditions)).all()

                if results:
                    data = {
                        "success": True,
                        "data": [{
                            "id": result.id,
                            "projectId": result.projectId,
                            "data": result.data,
                            "timestamp": str(result.timestamp),
                            "status": result.status,
                            "name": result.name,
                            "tags": result.tags,
                            "description": result.description,
                            "radius": result.radius,
                            "scale": result.scale,
                            "processedByMemberId": result.processedByMemberId
                        } for result in results]
                    }
                else:
                    data = {"success": False, "message": ["No results"]}
        except Exception as ex:
            data = {"success": False, "message": [str(ex)]}
        return anomalies_pb2.ReadAnomaliesResponse(**data)

    def UpdateRecordAnomalies(self, request, context):
        try:
            with Session() as session:
                conditions = []
                if request.id:
                    conditions.append(projects.c.id.in_(request.id))
                if request.projectId:
                    conditions.append(
                        projects.c.projectid.in_(request.projectid))
                if request.timestamp:
                    conditions.append(projects.c.timestamp.in_(
                        datetime.fromisoformat(request.timestamp)))
                if request.status:
                    conditions.append(projects.c.status.in_(request.status))
                if request.name:
                    conditions.append(projects.c.name.in_(request.name))
                if request.tags:
                    conditions.append(projects.c.tags.in_(request.tags))
                if request.description:
                    conditions.append(
                        projects.c.description.in_(request.description))
                if request.radius:
                    conditions.append(
                        projects.c.radius.in_(request.radius))
                if request.scale:
                    conditions.append(
                        projects.c.scale.in_(request.scale))
                if request.processedByMemberId:
                    conditions.append(
                        projects.c.processedByMemberId.in_(request.processedByMemberId))

                if not session.query(projects).filter(or_(*conditions)).count():
                    return anomalies_pb2.UpdateAnomaliesResponse(success=False, message=["No matching records found."])

                update_data = {
                    "projectid": request.update_data.projectid if request.update_data.projectid else None,
                    "data": request.update_data.data if request.update_data.data else None,
                    "status": request.update_data.status if request.update_data.status else None,
                    "name": request.update_data.name if request.update_data.name else None,
                    "tags": request.update_data.tags if request.update_data.tags else None,
                    "description": request.update_data.description if request.update_data.description else None,
                    "radius": request.update_data.radius if request.update_data.radius else None,
                    "scale": request.update_data.scale if request.update_data.scale else None,
                    "proceddedByMemberId": request.update_data.proceddedByMemberId if request.update_data.proceddedByMemberId else None,

                }

                if any(update_data.values()):
                    update_query = projects.update().where(or_(*conditions)).values(
                        **{k: v for k, v in update_data.items() if v is not None}
                    )
                    session.execute(update_query)
                    session.commit()
                    result = {"success": True, "message": ["Record updated"]}
                else:
                    result = {"success": False,
                              "message": ["No parameters to update."]}
        except Exception as ex:
            result = {"success": False, "message": [str(ex)]}

        return anomalies_pb2.UpdateAnomaliesResponse(**result)

    def DeleteRecordAnomalies(self, request, context):
        try:
            with Session() as session:
                conditions = []
                if request.id:
                    conditions.append(projects.c.id.in_(request.id))
                if request.projectId:
                    conditions.append(
                        projects.c.projectid.in_(request.projectid))
                if request.timestamp:
                    conditions.append(projects.c.timestamp.in_(
                        datetime.fromisoformat(request.timestamp)))
                if request.status:
                    conditions.append(projects.c.status.in_(request.status))
                if request.name:
                    conditions.append(projects.c.name.in_(request.name))
                if request.tags:
                    conditions.append(projects.c.tags.in_(request.tags))
                if request.description:
                    conditions.append(
                        projects.c.description.in_(request.description))
                if request.radius:
                    conditions.append(
                        projects.c.radius.in_(request.radius))
                if request.scale:
                    conditions.append(
                        projects.c.scale.in_(request.scale))
                if request.processedByMemberId:
                    conditions.append(
                        projects.c.processedByMemberId.in_(request.processedByMemberId))

                if not session.query(anomalies).filter(or_(*conditions)).count():
                    return anomalies_pb2.DeleteAnomaliesResponse(success=False, message=["No matching records found."])

                if conditions:
                    delete_query = anomalies.delete().where(or_(*conditions))
                    message = "Record deleted."
                else:
                    delete_query = anomalies.delete()
                    message = "Records deleted."
                session.execute(delete_query)
                session.commit()
                result = {"success": True, "message": [message]}
        except Exception as ex:
            result = {"success": False, "message": [str(ex)]}

        return anomalies_pb2.DeleteProjectsResponse(**result)
