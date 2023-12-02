from datetime import datetime
from utils.imports import projects_pb2_grpc, sessionmaker, projects_pb2, or_
from database.engine import engine
from database.tables import projects
from server_functions.servicers.check_input_functions import *
Session = sessionmaker(bind=engine)


class ProjectServicer(projects_pb2_grpc.ProjectsServiceServicer):
    def __init__(self):
        self.required_fields = ['name', 'description', 'status']
        self.string_fields = ['name', 'description']
        self.numeric_fields = ['status']
    
    def CreateRecordProjects(self, request, context):
        try:
            # check required fields
            success, field_name = check_required_fields(request, self.required_fields)
            if not success:
                data = {"success": success, "message": [f'Error: <{field_name}> is required but not provided.']}
                return projects_pb2.CreateProjectsResponse(**data)
            
            # check if string fields are not empty
            success, field_name = check_string_fields(request, self.string_fields)
            if not success:
                data = {"success": success, "message": [
                    f'Error: <{field_name}> cannot be empty or include whitespaces only.']}
                return projects_pb2.CreateProjectsResponse(**data)
            
            # check if value in allowed range
            success, field_name = check_integer_in_range(request.status, (0, 1))
            if not success:
                data = {"success": False, "message": [
                    f'Error: <status> cannot be {request.status}. Only allowed values - 0 or 1']}
                return projects_pb2.CreateProjectsResponse(**data)
        
            with Session() as session:
                # do database query
                new_record = projects.insert().values(
                    name=request.name,
                    description=request.description,
                    status=request.status
                )
                session.execute(new_record)
                session.commit()
                result = {"success": True, "message": ["Record created"]}
        except Exception as e:
            result = {"success": False, "message": [str(e)]}
        return projects_pb2.CreateProjectsResponse(**result)

    def ReadRecordProjects(self, request, context):
     #   try:
            with Session() as session:
                conditions = []
                conditions, error_messages = build_conditions(request)

                if error_messages:
                    return projects_pb2.ReadProjectsResponse({"success": False, "message": error_messages})

                results = build_query(session, conditions)

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
                    data = {"success": False, "message": ["No results"]}
      #  except Exception as ex:
      #      data = {"success": False, "message": [str(ex)]}
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
                    return projects_pb2.UpdateProjectsResponse(success=False, message=["No matching records found."])

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
                    result = {"success": True, "message": ["Record updated"]}
                else:
                    result = {"success": False,
                            "message": ["No parameters to update."]}
        except Exception as ex:
            result = {"success": False, "message": [str(ex)]}

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
                    return projects_pb2.DeleteProjectsResponse(success=False, message=["No matching records found."])

                if conditions:
                    delete_query = projects.delete().where(or_(*conditions))
                    message = "Record deleted."
                else:
                    delete_query = projects.delete()
                    message = "Records deleted."
                session.execute(delete_query)
                session.commit()
                result = {"success": True, "message": [message]}
        except Exception as ex:
            result = {"success": False, "message": [str(ex)]}

        return projects_pb2.DeleteProjectsResponse(**result)


def build_conditions(request):
    conditions = []

    def add_condition(field, values, check_func=None):
        if request.HasField(field):
            field_values = getattr(request, field).split(',')
            if field_values and check_func(field_values):
                conditions.append(values.in_(field_values))
            else:
                error_messages.append(
                    f'Error: <{field}> has incorrect format.')

    error_messages = []

    add_condition('id', projects.c.id, check_is_numeric_positive_list)
    if request.HasField('name'):
        field_values = request.name.split(',')
        success, field_name = check_string_fields(request=request, fields=field_values)
        if  success == True:
            conditions.append(projects.c.name.in_(field_values))
        else:
            error_messages.append(
                f'Error: <{field_name}> has incorrect format.')
    if request.HasField('description'):
        field_values = request.name.split(',')
        success, field_name = check_string_fields(
            request=request, fields=field_values)
        if success == True:
            conditions.append(projects.c.description.in_(field_values))
        else:
            error_messages.append(
                f'Error: <{field_name}> has incorrect format.')          
    add_condition('timestamp', projects.c.timestamp, check_is_valid_timestamp)
    add_condition('status', projects.c.status, check_is_status_int_in_range)
    return conditions, error_messages


def build_query(session, conditions):
    if not conditions:
        return session.query(projects).all()
    return session.query(projects).filter(or_(*conditions)).all()

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
