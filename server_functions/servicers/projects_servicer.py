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
            success, field_name = check_required_fields(
                request, self.required_fields)
            if not success:
                data = {"success": success, "message": [
                    f'Error: <{field_name}> is required but not provided.']}
                return projects_pb2.CreateProjectsResponse(**data)

            # check if string fields are not empty
            success, field_name = check_string_fields(
                request, self.string_fields)
            if not success:
                data = {"success": success, "message": [
                    f'Error: <{field_name}> cannot be empty or include whitespaces only.']}
                return projects_pb2.CreateProjectsResponse(**data)

            # check if value in allowed range
            success, field_name = check_integer_in_range(
                request.status, (0, 1))
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
        try:
            with Session() as session:
                conditions = []
                conditions, error_messages = build_conditions(request)
                if error_messages:
                    return projects_pb2.ReadProjectsResponse({"success": False, "message": error_messages, "data": []})

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
        except Exception as ex:
            data = {"success": False, "message": [str(ex)]}
        return projects_pb2.ReadProjectsResponse(**data)

    def UpdateRecordProjects(self, request, context):
        try:
            conditions, error_messages, update_data = build_conditions_and_update_data(
                request)
            if error_messages:
                return projects_pb2.UpdateProjectsResponse({"success": False, "message": error_messages})
            with Session() as session:
                if conditions:
                    execute_update_query(session, conditions, update_data)
                    result = {"success": True, "message": ["Record updated"]}
                else:
                    result = {"success": False, "message": [
                        "No conditions provided for update"]}
        except Exception as ex:
            result = {"success": False, "message": [str(ex)]}
        return projects_pb2.UpdateProjectsResponse(**result)

    def DeleteRecordProjects(self, request, context):
        try:
            conditions, error_messages = build_conditions(request)
            if error_messages:
                return projects_pb2.DeleteProjectsResponse({"success": False, "message": error_messages})
            with Session() as session:
                execute_delete_query(session, conditions)
                result = {"success": True, "message": ['Record deleted']}
        except Exception as ex:
            result = {"success": False, "message": [str(ex)]}

        return projects_pb2.DeleteProjectsResponse(**result)


def execute_delete_query(session, conditions):
    if conditions:
        if not session.query(projects).filter(or_(*conditions)).count():
            raise ValueError("No matching records found.")
        delete_query = projects.delete().where(or_(*conditions))
    else:
        delete_query = projects.delete()
    session.execute(delete_query)
    session.commit()


def execute_update_query(session, conditions, update_data_dict):
    if not session.query(projects).filter(or_(*conditions)).count():
        raise ValueError("No matching records found.")

    update_query = projects.update().where(or_(*conditions)).values(
        **{k: v for k, v in update_data_dict.items() if v is not None}
    )
    session.execute(update_query)
    session.commit()
    session.execute(update_query)
    session.commit()


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
        success, field_name = check_string_lists(fields=field_values)
        if success == True:
            conditions.append(projects.c.name.in_(field_values))
        else:
            error_messages.append(
                f'Error: <{field_name}> has incorrect format.')
    if request.HasField('description'):
        field_values = request.name.split(',')
        success, field_name = check_string_lists(fields=field_values)
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


def build_conditions_and_update_data(request):
    conditions, error_messages = build_conditions(request)
    update_data = {}

    if request.HasField('update_data'):
        validate_update_data(request.update_data, error_messages, update_data)

    return conditions, error_messages, update_data


def validate_update_data(update_data, error_messages, update_data_dict):
    if update_data.HasField('name'):
        if not check_string_is_not_empty(update_data.name):
            error_messages.append(
                'Error: <name> values are empty or consist of whitespaces only.')
        else:
            update_data_dict["name"] = update_data.name

    if update_data.HasField('description'):
        if not check_string_is_not_empty(update_data.description):
            error_messages.append(
                'Error: <description> values are empty or consist of whitespaces only.')
        else:
            update_data_dict["description"] = update_data.description

    if update_data.HasField('status'):
        if not check_is_status_int_in_range([update_data.status]):
            error_messages.append(
                'Error: <status> values are not integers or are not in (0, 1).')
        else:
            update_data_dict["status"] = update_data.status

    if not any(update_data_dict.values()):
        error_messages.append('Error: No parameters to update.')
