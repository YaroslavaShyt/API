from datetime import datetime
from utils.imports import anomalies_pb2_grpc, anomalies_pb2, sessionmaker, or_
from database.engine import engine
from database.tables import projects, anomalies, project_members
from server_functions.servicers.check_input_functions import *

Session = sessionmaker(bind=engine)


class AnomaliesServicer(anomalies_pb2_grpc.AnomaliesServiceServicer):
    def __init__(self):
        super().__init__()
        self.required_fields    = ['projectId', 'data', 'status','name', 'tags', 'radius', 'scale', 'processedByMemberId']
        self.string_fields      = ['name', 'tags', 'data']
        self.integer_fields     = ['projectId', 'status', 'radius', 'scale']
        self.other_table_values = {projects: None, project_members: None}

    def CreateRecordAnomalies(self, request, context):
        # define field types for better check-outs

        try:
            # check if all required fields were given
            success, field_name = check_required_fields(
                request, self.required_fields)
            if not success:
                return anomalies_pb2.CreateAnomaliesResponse({"success": success, "message": [f'Error: <{field_name}> is required but not provided.']})

            # <description> is not required
            if request.HasField('description'):
                self.string_fields.append('description')

            # check if string fields are not empty
            success, field_name = check_string_fields(
                request, self.string_fields)
            if not success:
                return anomalies_pb2.CreateAnomaliesResponse({"success": success, "message": [f'Error: <{field_name}> cannot be empty or include whitespaces only.']})

            # check integer values > 0
            success, field_name = check_integer_fields(
                request, self.integer_fields)
            if not success:
                return anomalies_pb2.CreateAnomaliesResponse({"success": success, "message": [f'Error: <{field_name}> cannot be below zero.']})

            # check if value in allowed range
            success, field_name = check_integer_in_range(
                request.status, (0, 1))
            if not success:
                return anomalies_pb2.CreateAnomaliesResponse({"success": False, "message": ['Error: <status> cannot be "{request.status}". Only allowed values - 0 or 1']})

            with Session() as session:
                # check if database values exist
                self.other_table_values[projects] = request.projectId
                self.other_table_values[project_members] = request.processedByMemberId
                self.success, field_name, = check_id_in_table(
                    session, self.other_table_values)
                if not success:
                    if field_name == projects:
                        field_name = 'projectsId'
                    elif field_name == project_members:
                        field_name = 'processedByMemberId'
                    field_value = getattr(request, field_name, None)
                    return anomalies_pb2.CreateAnomaliesResponse({"success": success, "message": [f"No matching records found for {field_name} <{field_value}>."]})

                # do insert query
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
                conditions, error_messages = build_conditions(request)

                if error_messages:
                    return anomalies_pb2.ReadAnomaliesResponse({"success": False, "message": error_messages})

                results = build_query(session, conditions)

                if results:
                    data = {
                        "success": True,
                        "message": ['Found records.'],
                        "data": [{
                            "id": result.id,
                            "projectId": result.projectid,
                            "data": result.data,
                            "timestamp": str(result.timestamp),
                            "status": result.status,
                            "name": result.name,
                            "tags": result.tags,
                            "description": result.description,
                            "radius": result.radius,
                            "scale": result.scale,
                            "processedByMemberId": result.processedByMemberId
                        } for result in results]}
                else:
                    data = {"success": False, "message": ["No results"]}
        except Exception as ex:
            data = {"success": False, "message": [str(ex)]}
        return anomalies_pb2.ReadAnomaliesResponse(**data)

    def UpdateRecordAnomalies(self, request, context):
        try:
            with Session() as session:
                conditions, error_messages, update_data = build_conditions_and_update_data(
                    request)

                if request.HasField('update_data'):
                    validate_update_data(request.update_data,
                                        error_messages, update_data)

                if error_messages:
                    return anomalies_pb2.UpdateAnomaliesResponse({"success": False, "message": error_messages})

                if conditions:
                    execute_update_query(session, conditions, update_data)
                    result = {"success": True, "message": ["Record updated"]}
                else:
                    result = {"success": False, "message": [
                        "No conditions provided for update"]}

        except Exception as ex:
            result = {"success": False, "message": [str(ex)]}
        return anomalies_pb2.UpdateAnomaliesResponse(**result)

    def DeleteRecordAnomalies(self, request, context):
        try:
            with Session() as session:
                conditions, error_messages = build_conditions(request)

                if error_messages:
                    return anomalies_pb2.DeleteAnomaliesResponse({"success": False, "message": error_messages})

                if conditions:
                    execute_delete_query(session, conditions)
                    result = {"success": True, "message": ["Record deleted"]}
                else:
                    result = {"success": False, "message": [
                        "No conditions provided for delete"]}

        except Exception as ex:
            result = {"success": False, "message": [str(ex)]}

        return anomalies_pb2.DeleteAnomaliesResponse(**result)


def build_conditions(request):
    conditions = []

    def add_condition(field, values, check_func):
        if request.HasField(field):
            field_values = getattr(request, field).split(',')
            if field_values and check_func(field_values):
                conditions.append(values.in_(field_values))
            else:
                error_messages.append(
                    f'Error: <{field}> has incorrect format.')

    error_messages = []

    add_condition('id', anomalies.c.id, check_is_numeric_positive_list)
    add_condition('projectId', projects.c.id, check_is_numeric_positive_list)
    add_condition('timestamp', anomalies.c.timestamp, check_is_valid_timestamp)
    add_condition('status', anomalies.c.status, check_is_status_int_in_range)
    add_condition('name', anomalies.c.name, check_string_is_not_empty)
    add_condition('tags', anomalies.c.tags, check_string_is_not_empty)
    add_condition('description', anomalies.c.description,
                  check_string_is_not_empty)
    add_condition('radius', anomalies.c.radius, check_is_numeric_positive_list)
    add_condition('scale', anomalies.c.scale, check_is_numeric_positive_list)
    add_condition('processedByMemberId',
                  anomalies.c.processedByMemberId, check_is_numeric_positive_list)

    return conditions, error_messages


def build_query(session, conditions):
    if not conditions:
        return session.query(anomalies).all()
    return session.query(anomalies).filter(or_(*conditions)).all()


def build_conditions_and_update_data(request):
    conditions, error_messages = build_conditions(request)
    update_data = {}

    if request.HasField('update_data'):
        if request.update_data.HasField('projectId'):
            validate_project_id_for_update(
                request.update_data, conditions, error_messages, update_data)

        validate_update_data(request.update_data, error_messages, update_data)

    return conditions, error_messages, update_data


def validate_project_id_for_update(update_data, conditions, error_messages, update_data_dict):
    if not check_is_numeric_positive_list([update_data.projectId]):
        error_messages.append(
            'Error: some <id> values are not integers or are negative.')
    else:
        conditions = [projects.c.id.in_([update_data.projectId])]
        if not Session.query(projects).filter(or_(*conditions)).count():
            error_messages.append(
                f"No matching records found for projectId <{update_data.projectId}>")
        else:
            update_data_dict["projectId"] = update_data.projectId


def execute_update_query(session, conditions, update_data_dict):
    if not session.query(anomalies).join(projects, anomalies.c.projectid == projects.c.id).filter(or_(*conditions)).count():
        raise ValueError("No matching records found.")

    update_query = projects.update().where(or_(*conditions)).values(
        **{k: v for k, v in update_data_dict.items() if v is not None}
    )
    session.execute(update_query)
    session.commit()


def execute_delete_query(session, conditions):
    if not session.query(anomalies).filter(or_(*conditions)).count():
        raise ValueError("No matching records found.")

    delete_query = anomalies.delete().where(or_(*conditions))
    session.execute(delete_query)
    session.commit()
