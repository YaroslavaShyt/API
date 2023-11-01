from utils.imports import service_pb2


async def create_record(stub, data):
    response = await stub.CreateRecordProjects(service_pb2.CreateRequestProjects(**data))
    return response


async def read_record(stub, data):
    response = await stub.ReadRecordProjects(service_pb2.ReadRequestProjects(**data))
    return response


async def update_record(stub, data):
    response = await stub.UpdateRecordProjects(service_pb2.UpdateRequestProjects(**data))
    return response


async def delete_record(stub, data):
    response = await stub.DeleteRecordProjects(service_pb2.DeleteRequestProjects(**data))
    return response
