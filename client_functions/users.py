from utils.imports import projects_pb2, users_pb2


async def create_record_users(stub, data):
    response = await stub.CreateRecordUsers(users_pb2.CreateRequestUsers(**data))
    return response


async def read_record_users(stub, data):
    response = await stub.ReadRecordUsers(users_pb2.ReadRequestUsers(**data))
    return response


async def update_record_users(stub, data):
    response = await stub.UpdateRecordUsers(users_pb2.UpdateRequestUsers(**data))
    return response


async def delete_record_users(stub, data):
    response = await stub.DeleteRecordUsers(users_pb2.DeleteRequestUsers(**data))
    return response
