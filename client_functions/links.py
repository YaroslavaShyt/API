from utils.imports import links_pb2


async def create_record_links(stub, data):
    response = await stub.CreateRecordLinks(links_pb2.CreateLinksRequest(**data))
    return response


async def read_record_links(stub, data):
    response = await stub.ReadRecordLinks(links_pb2.ReadLinksRequest(**data))
    return response


async def update_record_links(stub, data):
    response = await stub.UpdateRecordLinks(links_pb2.UpdateLinksRequest(**data))
    return response


async def delete_record_links(stub, data):
    response = await stub.DeleteRecordLinks(links_pb2.DeleteLinksRequest(**data))
    return response