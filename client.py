from utils.imports import projects_pb2_grpc, grpc, asyncio, users_pb2_grpc
from client_functions.projects import *
from client_functions.users import *


async def run() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        # USERS
        stub = users_pb2_grpc.UserServiceStub(channel)
        print(f"Create record users:")
        create_result = await create_record_users(
            stub, {"name": "PROJECT",
                   "key": "92e01118-bdfd-4b".encode('utf-8'),
                   "hash": "5b3ad3145fd1518a9f8742c5fa850b60a6b82774e47bf8edf3d1ffc0d339701b".encode('utf-8'),
                   "salt": "salt",
                   "status": 1,
                   "description": "description",
                   })
        print(create_result)

        print(f"Read record users:")
        read_result = await read_record_users(stub, {"id": 2})
        print(read_result)

        print(f"Update result users:")
        update_result = await update_record_users(
            stub, {"id": 3, "name": "newname", "description": "newdescription", })
        print(update_result)

        print(f"Delete result users:")
        delete_result = await delete_record_users(stub, {"id": 1})
        print(delete_result)

        # PROJECTS
        stub = projects_pb2_grpc.ProjectsServiceStub(channel)

        print(f"Create record projects:")
        create_result = await create_record_projects(
            stub, {"name": "PROJECT", "description": "test project 1", "status": "active"})
        print(create_result)

        print(f"Read record projects:")
        read_result = await read_record_projects(stub, {"id": 3})
        print(read_result)

        print(f"Update result projects:")
        update_result = await update_record_projects(
            stub, {"id": 1, "name": "newname", "description": "newdescription", "status": "newstatus"})
        print(update_result)

        print(f"Delete result projects:")
        delete_result = await delete_record_projects(stub, {"id": 1})
        print(delete_result)


if __name__ == "__main__":
    asyncio.run(run())
