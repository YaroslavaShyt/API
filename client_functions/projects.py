from utils.imports import projects_pb2


def check_data_params(param_name, list_type, data):
    if param_name in data:
        if not isinstance(data[param_name], list) or not all(isinstance(x, list_type) for x in data[param_name]) or not data[param_name]:
            return f"Error: invalid '{param_name}' value. Expected a non-empty list of {list_type}."
    return ''

def check_projects_data(data):
    error_messages = []
    if not isinstance(data, dict):
        error_messages.append(
            f'Error: incorrect type for data transfer - {type(data)}. Expected - dictionary.')
    else:
        error = check_data_params("id", int, data)
        if error:
            error_messages.append(error)
        error = check_data_params("name", str, data)
        if error:
            error_messages.append(error)
        error = check_data_params("description", str, data)
        if error:
            error_messages.append(error)
        error = check_data_params("status", int, data)
        if error:
            error_messages.append(error)
        error = check_data_params("timestamp", int, data)
        if error:
            error_messages.append(error)
    return error_messages


async def create_record_projects(stub, data):
    error_messages = []

    if not isinstance(data, dict):
        error_messages.append(
            f'Error: incorrect type for data transfer - {type(data)}. Expected - dictionary.')
    else:
        # check <Name>
        if "name" not in data or not isinstance(data["name"], str) or not data["name"].strip():
            if "name" not in data:
                error_messages.append('Error: no <Name> parameter provided.')
            elif not isinstance(data["name"], str):
                error_messages.append(
                    f'Error: parameter <Name> has unexpected type - {type(data["name"])}. Expected - string.')
            else:
                error_messages.append(
                    'Error: parameter <Name> cannot be empty or have whitespaces only.')

        # check <Description>
        if "description" not in data or not isinstance(data["description"], str) or not data["description"].strip():
            if "description" not in data:
                error_messages.append(
                    'Error: no <Description> parameter provided.')
            elif not isinstance(data["description"], str):
                error_messages.append(
                    f'Error: parameter <Description> has unexpected type - {type(data["description"])}. Expected - string.')
            else:
                error_messages.append(
                    'Error: parameter <Description> cannot be empty or have whitespaces only.')

        # check <Status>
        if "status" not in data or not isinstance(data["status"], int):
            if "status" not in data:
                error_messages.append('Error: no <Status> parameter provided.')
            elif not isinstance(data["status"], int):
                error_messages.append(
                    f'Error: parameter <Status> has unexpected type - {type(data["status"])}. Expected - integer.')

    # if errors - do not send request
    if error_messages:
        return {"success": False, "message": error_messages}
    else:
        # if no errors - send request
        response = await stub.CreateRecordProjects(projects_pb2.CreateProjectsRequest(**data))
        return response


async def read_record_projects(stub, data):
    #error_messages = check_projects_data(data)
    #if error_messages:
    #    return {"success": False, "message": error_messages}
    #else:
        response = await stub.ReadRecordProjects(projects_pb2.ReadProjectsRequest(**data))
        return response


async def update_record_projects(stub, data):
   # error_messages = check_projects_data(data)
    #if error_messages:
     #   return {"success": False, "message": error_messages}
    #else:
        response = await stub.UpdateRecordProjects(projects_pb2.UpdateProjectsRequest(**data))
        return response


async def delete_record_projects(stub, data):
    error_messages = check_projects_data(data)
    if error_messages:
        return {"success": False, "message": error_messages}
    else:
        response = await stub.DeleteRecordProjects(projects_pb2.DeleteProjectsRequest(**data))
        return response
