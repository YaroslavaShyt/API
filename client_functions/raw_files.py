from utils.imports import raw_files_pb2


async def create_record_raw_files(stub, data):
    response = await stub.CreateRecordRawFiles(raw_files_pb2.CreateRequestRawFiles(**data))
    return response


async def read_record_raw_files(stub, data):
    response = await stub.ReadRecordRawFiles(raw_files_pb2.ReadRequestRawFiles(**data))
    return response


async def update_record_raw_files(stub, data):
    response = await stub.UpdateRecordRawFiles(raw_files_pb2.UpdateRequestRawFiles(**data))
    return response


async def delete_record_raw_files(stub, data):
    response = await stub.DeleteRecordRawFiles(raw_files_pb2.DeleteRequestRawFiles(**data))
    return response
