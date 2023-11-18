from utils.imports import projects_pb2

def check_data_params(data):
    error_messages = []
    if not isinstance(data, dict):
        error_messages.append(
            f'Error: incorrect type for data transfer - {type(data)}. Expected - dictionary.')
    else:
        if "id" in data:
                if not isinstance(data["id"], list) or not all(isinstance(x, int) for x in data["id"]) or not data["id"]:
                    error_messages.append(
                        "Error: invalid 'id' value. Expected a non-empty list of integers.")
        if "name" in data:
                if not isinstance(data["name"], list) or not all(isinstance(x, str) for x in data["name"]) or not data["name"]:
                    error_messages.append(
                        "Error: invalid 'name' value. Expected a non-empty list of strings.")

        if "description" in data:
                if not isinstance(data["description"], list) or not all(isinstance(x, str) for x in data["description"]) or not data["description"]:
                    error_messages.append(
                        "Error: invalid 'description' value. Expected a non-empty list of strings.")
        if "timestamp" in data:
                if not isinstance(data["timestamp"], list) or not all(isinstance(x, str) for x in data["timestamp"]) or not data["timestamp"]:
                    error_messages.append(
                        "Error: invalid 'timestamp' value. Expected a non-empty list of strings.")

        if "status" in data:
                if not isinstance(data["status"], list) or not all(isinstance(x, int) for x in data["status"]) or not data["status"]:
                    error_messages.append(
                        "Error: invalid 'status' value. Expected a non-empty list of integers.")
    return error_messages


async def create_record_projects(stub, data):
    error_messages = []

    if not isinstance(data, dict):
        error_messages.append(f'Error: incorrect type for data transfer - {type(data)}. Expected - dictionary.')
    else:
        # check <Name>
        if "name" not in data or not isinstance(data["name"], str) or not data["name"].strip():
            if "name" not in data:
                error_messages.append('Error: no <Name> parameter provided.')
            elif not isinstance(data["name"], str):
                error_messages.append(f'Error: parameter <Name> has unexpected type - {type(data["name"])}. Expected - string.')
            else:
                error_messages.append('Error: parameter <Name> cannot be empty or have whitespaces only.')

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
    error_messages = check_data_params(data)
    if error_messages:
        return {"success": False, "message": error_messages}
    else:
        response = await stub.ReadRecordProjects(projects_pb2.ReadProjectsRequest(**data))
        return response



async def update_record_projects(stub, data):
    error_messages = check_data_params(data)
    if error_messages:
        return {"success": False, "message": error_messages}
    else:
        response = await stub.UpdateRecordProjects(projects_pb2.UpdateProjectsRequest(**data))
        return response


async def delete_record_projects(stub, data):
    error_messages = check_data_params(data)
    if error_messages:
        return {"success": False, "message": error_messages}
    else:
        response = await stub.DeleteRecordProjects(projects_pb2.DeleteProjectsRequest(**data))
        return response
