from utils.imports import projects_pb2_grpc, grpc, asyncio, users_pb2_grpc, raw_files_pb2_grpc, anomalies_pb2_grpc
from client_functions.projects import *
from client_functions.users import *
from client_functions.anomalies import *
from client_functions.raw_files import *
import pandas as pd


def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    csv_content = df.to_csv(index=False)
    return bytes(csv_content, 'utf-8')


async def run() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        # ANOMALIES
        stub = anomalies_pb2_grpc.AnomaliesServiceStub(channel)
        print(f"Create record anomalies:")
        create_result = await create_record_anomalies(
            stub, {#"projectId": 4, 
                   "data": "5b3ad3145fd1518a9f8742c5fa850b60a6b82774e47bf8edf3d1ffc0d339701b".encode('utf-8'), 
                   "status": 0,
                   "name": "Name", 
                   "tags": "tags",
                   "description": "test project 1", 
                   "radius": 3,
                   "scale": 5,
                   "processedByMemberId": 1
                   })
        print(create_result)
       
"""
        print(f"Read record anomalies:")
        read_result = await read_record_anomalies(stub, {})
        print(read_result)
       

        print(f"Delete result anomalies:")
        delete_result = await delete_record_anomalies(stub, {"id": [100000000]})
        print(delete_result)

        

        print(f"Update result anomalies:")
        update_result = await update_record_anomalies(
            stub, {"id": [1], "update_data": {"name": "newname", "description": "newdescription", "status": 1}})
        print(update_result)

       
# PROJECTS
        stub = projects_pb2_grpc.ProjectsServiceStub(channel)
        print(f"Delete result projects:")
        delete_result = await delete_record_projects(stub, {"id": [100000000]})
        print(delete_result)
 print(f"Read record projects:")
        read_result = await read_record_projects(stub, {})
        print(read_result)

        print(f"Create record projects:")
        create_result = await create_record_projects(
                    stub, {"name": "Name", "description": "test project 1", "status": 0})
        print(create_result)

        print(f"Update result projects:")
        update_result = await update_record_projects(
            stub, {"id": [1], "update_data": {"name": "newname", "description": "newdescription", "status": 1}})
        print(update_result)

        
"""

"""
       # USERS
        stub = users_pb2_grpc.UserServiceStub(channel)
        print(f"Create record users:")
        create_result = await create_record_users(
            stub, {"name": "PROJECT",
                   "username": "username",
                   "key": "92e01118-bdfd-4b".encode('utf-8'),
                   "hash": "5b3ad3145fd1518a9f8742c5fa850b60a6b82774e47bf8edf3d1ffc0d339701b".encode('utf-8'),
                   "salt": "salt",
                   "status": 1,
                   "description": "description",
                   })
        print(create_result)

        print(f"Read record users:")
        read_result = await read_record_users(stub, {})
        print(read_result)

        print(f"Update result users:")
        update_result = await update_record_users(
            stub, {"id": [3], "update_data": {"name": "newname", "description": "newdescription"}})
        print(update_result)

        print(f"Delete result users:")
        delete_result = await delete_record_users(stub, {"id": [1]})
        print(delete_result)

        
        

        


        stub = raw_files_pb2_grpc.RawFilesServiceStub(channel)
        print(f"Create record raw files:")
        data_bytes = read_csv_file("test_data/very_very_long_data.csv")
        create_result = await create_record_raw_files(
            stub, {"project_id": 3,
                   "data": data_bytes,
                   "status": 1
                   })
        print(create_result)
"""

if __name__ == "__main__":
    asyncio.run(run())
