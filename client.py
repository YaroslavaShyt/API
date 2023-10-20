from utils.imports import Struct, MessageToDict, service_pb2_grpc, service_pb2, grpc, asyncio


async def create_record(stub, data):
    struct = Struct()
    struct.update(data)
    response = await stub.CreateRecord(service_pb2.CreateRequest(data=struct))
    return MessageToDict(response.data)


async def read_record(stub, data):
    struct = Struct()
    struct.update(data)
    response = await stub.ReadRecord(service_pb2.ReadRequest(data=struct))
    print(response.data)
    return MessageToDict(response.data)


async def update_record(stub, data):
    struct = Struct()
    struct.update(data)
    response = await stub.UpdateRecord(service_pb2.UpdateRequest(data=struct))
    return MessageToDict(response.data)


async def delete_record(stub, data):
    struct = Struct()
    struct.update(data)
    response = await stub.DeleteRecord(service_pb2.DeleteRequest(data=struct))
    return MessageToDict(response.data)


async def run() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = service_pb2_grpc.DatabaseServiceStub(channel)
        record_id = await create_record(
            stub, {"name": "project 1", "description": "test project 1", "status": "active"})
        print(f"Created record with ID {record_id}\n\n")

        record = await read_record(stub, {"id": 2})
        print(f"Read record: {record}\n\n")

        update_result = await update_record(
            stub, {"id": 1, "name": "newname", "description": "newdescription", "status": "newstatus"})
        print(f"Update result: {update_result}\n\n")

        delete_result = await delete_record(stub, {"id": 1})
        print(f"Delete result: {delete_result}\n\n")



if __name__ == "__main__":
    asyncio.run(run())
