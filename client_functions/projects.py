from utils.imports import projects_pb2


async def create_record_projects(stub, data):
    response = await stub.CreateRecordProjects(projects_pb2.CreateRequestProjects(**data))
    return response


async def read_record_projects(stub, data):
    response = await stub.ReadRecordProjects(projects_pb2.ReadRequestProjects(**data))
    return response


async def update_record_projects(stub, data):
    response = await stub.UpdateRecordProjects(projects_pb2.UpdateRequestProjects(**data))
    return response


async def delete_record_projects(stub, data):
    response = await stub.DeleteRecordProjects(projects_pb2.DeleteRequestProjects(**data))
    return response
