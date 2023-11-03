from utils.imports import projects_pb2_grpc, grpc, asyncio, users_pb2_grpc
from client_functions.projects import *
from client_functions.users import *
from datetime import datetime


async def run() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:

       # stub = projects_pb2_grpc.ProjectsServiceStub(channel)
       # print(f"Create record:")
       # create_result = await create_record_projects(
       #     stub, {"name": "PROJECT", "description": "test project 1", "status": "active"})
       # print(create_result)

        stub = users_pb2_grpc.UserServiceStub(channel)
        print(f"Create record users:")
        create_result = await create_record_users(
            stub, {"name": "PROJECT",
                   "key": bytes.fromhex("123456"),
                   "hash": bytes.fromhex("123456"),
                   "salt": "salt",
                   "status": 1,
                   "description": "description",
                   })
        print(create_result)
        """
        print(f"Create record users:")
        create_result = await create_record_users(
            stub, {"name": "PROJECT",
                   "key": bytes.fromhex("123456"),
                   "hash": bytes.fromhex("123456"),
                   "salt": "salt",
                   "status": 1,
                   "description": "description",
                   "timestamp": str(datetime.today())})
        print(create_result)

        print(f"Read record users:")
        read_result = await read_record_users(stub, {"id": 3,
                                                     # "name": "name", "description": "description", "status": "active"
                                                     })
        print(read_result)

        print(f"Update result users:")
        update_result = await update_record_users(
            stub, {"id": 1, "name": "newname", "description": "newdescription", "status": "newstatus"})
        print(update_result)

        print(f"Delete result users:")
        delete_result = await delete_record_users(stub, {"id": 1})
        print(delete_result)

        print(f"Create record:")
        create_result = await create_record_projects(
            stub, {"name": "PROJECT", "description": "test project 1", "status": "active"})
        print(create_result)

        print(f"Read record:")
        read_result = await read_record_projects(stub, {"id": 3,
                                               # "name": "name", "description": "description", "status": "active"
                                               })
        print(read_result)

        print(f"Update result:")
        update_result = await update_record_projects(
            stub, {"id": 1, "name": "newname", "description": "newdescription", "status": "newstatus"})
        print(update_result)

        print(f"Delete result:")
        delete_result = await delete_record_projects(stub, {"id": 1})
        print(delete_result)
"""

if __name__ == "__main__":
    asyncio.run(run())
