from utils.imports import service_pb2_grpc, grpc, asyncio
from client_functions.client_functions import *


async def run() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = service_pb2_grpc.DatabaseServiceStub(channel)

        print(f"Create record:")
        create_result = await create_record(
            stub, {"name": "PROJECT", "description": "test project 1", "status": "active"})
        print(create_result)

        print(f"Read record:")
        read_result = await read_record(stub, {"id": 3,
                                               # "name": "name", "description": "description", "status": "active"
                                               })
        print(read_result)

        print(f"Update result:")
        update_result = await update_record(
            stub, {"id": 1, "name": "newname", "description": "newdescription", "status": "newstatus"})
        print(update_result)

        print(f"Delete result:")
        delete_result = await delete_record(stub, {"id": 1})
        print(delete_result)


if __name__ == "__main__":
    asyncio.run(run())
