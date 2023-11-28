from datetime import datetime
from utils.imports import anomalies_pb2_grpc, anomalies_pb2, sessionmaker, or_
from database.engine import engine
from database.tables import projects, anomalies, project_members
from service import *
Session = sessionmaker(bind=engine)


class AnomaliesServicer(anomalies_pb2_grpc.AnomaliesServiceServicer):
    def CreateRecordAnomalies(self, request, context):
        error_messages = []
        try:
            with Session() as session:

                # check <ProjectId>
                if request.HasField('projectId'):
                    conditions = [projects.c.id.in_([request.projectId])]
                    if not session.query(projects).filter(or_(*conditions)).count():
                        error_messages.append(
                            f"No matching records found for projectId <{request.id}>")
                else:
                    error_messages.append(
                        'Error: <projectId> is required but not provided.')

                # check <Data>
                if request.HasField('data'):
                    if not request.data:
                        error_messages.append('Error: <data> is empty.')
                else:
                    error_messages.append(
                        'Error: <data> is required but not provided.')

                # check <Status>
                if request.HasField('status'):
                    if request.status not in (0, 1):
                        error_messages.append(
                            f'Error: <status> cannot be "{request.status}". Only allowed values - 0 or 1')
                else:
                    error_messages.append(
                        'Error: <status> is required but not provided.')

                # check <Name>
                if request.HasField('name'):
                    if not request.name or not request.name.strip():
                        error_messages.append(
                            'Error: <name> cannot be empty or include whitespaces only.')
                else:
                    error_messages.append(
                        'Error: <name> is required but not provided.')

                # check <Tags>
                if request.HasField('tags'):
                    if not request.tags or not request.tags.strip():
                        error_messages.append(
                            'Error: <tags> cannot be empty or include whitespaces only.')
                else:
                    error_messages.append(
                        'Error: <tags> is required but not provided.')

                # check <Description>
                if request.HasField('description'):
                    if not request.description or not request.description.strip():
                        error_messages.append(
                            'Error: <description> cannot be empty or include whitespaces only.')

                # check <Radius>
                if request.HasField('radius'):
                    if request.radius < 0:
                        error_messages.append(
                            'Error: <radius> cannot be below zero.')
                else:
                    error_messages.append(
                        'Error: <radius> is required but not provided.')

                # check <Scale>
                if request.HasField('scale'):
                    if request.scale < 0:
                        error_messages.append(
                            'Error: <scale> cannot be below zero.')
                else:
                    error_messages.append(
                        'Error: <scale> is required but not provided.')

                # check <ProcessedByMemberId>
                if request.HasField('processedByMemberId'):
                    conditions = [project_members.c.id.in_(
                        [request.projectId])]
                    if not session.query(project_members).filter(or_(*conditions)).count():
                        error_messages.append(
                            f'Error: No matching records found for processedByMemberId {request.projectId}.')
                else:
                    error_messages.append(
                        'Error: <processedByMemberId> is required but not provided.')

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
                            request.HasField('description')) else None,
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
                error_messages = []
                if request.HasField('id'):
                    ids = request.id.split(',')
                    if ids:
                        if check_is_numeric_positive_list(ids):
                            conditions.append(projects.c.id.in_(ids))
                        else:
                            error_messages.append(
                                'Error: some <id> values are not integers.')
                    else:
                        error_messages.append('Error: <id> has incorrect format.')
                if request.HasField('projectId'):
                    project_ids = request.projectId.split(',')
                    if project_ids:
                        if check_is_numeric_positive_list(project_ids):
                            conditions.append(projects.c.projectid.in_(project_ids))
                        else:
                            error_messages.append(
                                'Error: some <projectId> values are not integers.')
                    else:
                        error_messages.append(
                            'Error: <projectId> has incorrect format.')
                if request.HasField('timestamp'):
                    timestamps = request.projectId.split(',')
                    if timestamps:
                        conditions.append(projects.c.timestamp.in_(
                            datetime.fromisoformat(timestamps)))
                    else:
                        error_messages.append(
                            'Error: <timestamp> has incorrect format.')
                        
                if request.HasField('status'):
                    statuses = request.status.split(',')
                    if statuses:
                        if check_is_status_int_in_range(statuses):
                            conditions.append(projects.c.status.in_(request.status))
                        else:
                            error_messages.append(
                                'Error: <status> values are not integers or are not in (0, 1).')
                    else:
                        error_messages.append(
                            'Error: <timestamp> has incorrect format.')
                        
                if request.HasField('name'):
                    names = request.name.split(',')
                    if names:
                        if check_string_is_not_empty(names):
                            conditions.append(projects.c.name.in_(request.name))
                        else:
                            error_messages.append(
                                'Error: <name> values are empty or consist of whitespaces only.')
                    else:
                        error_messages.append(
                            'Error: <name> has incorrect format.')
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
                print(results)
                if results:
                    data = {
                        "success": True,
                        "message": 'Found records.',
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
            print('in ex')
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
