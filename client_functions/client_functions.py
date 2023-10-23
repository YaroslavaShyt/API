from utils.imports import service_pb2


async def create_record(stub, data):
    response = await stub.CreateRecord(service_pb2.CreateRequest(**data))
    return response


async def read_record(stub, data):
    response = await stub.ReadRecord(service_pb2.ReadRequest(**data))
    return response


async def update_record(stub, data):
    response = await stub.UpdateRecord(service_pb2.UpdateRequest(**data))
    return response


async def delete_record(stub, data):
    response = await stub.DeleteRecord(service_pb2.DeleteRequest(**data))
    return response
