import grpc
import asyncio
import service_pb2
import service_pb2_grpc
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST")
port = int(os.getenv("PORT"))
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
server_port = os.getenv("SERVER_PORT")


class YourServiceServicer(service_pb2_grpc.DatabaseServiceServicer):
    def __init__(self):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

    async def CreateRecord(self, request, context):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO projects (name, description, status) VALUES (%s, %s, %s)",
                       (request.name, request.description, request.status))
        self.connection.commit()
        cursor.close()
        return service_pb2.CreateResponse(message="Record created: insert into projects")

    async def ReadRecord(self, request, context):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = %s", (request.record_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return service_pb2.ReadResponse(data=result)
        else:
            return service_pb2.ReadResponse(data="Record not found")

    async def UpdateRecord(self, request, context):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE projects SET name = %s, description = %s, status = %s WHERE id = %s",
                       (request.name, request.description, request.status, request.record_id))
        self.connection.commit()
        cursor.close()
        return service_pb2.UpdateResponse(message="Record updated: projects table")

    async def DeleteRecord(self, request, context):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM projects WHERE id = %s", (request.record_id,))
        self.connection.commit()
        cursor.close()
        return service_pb2.DeleteResponse(message="Record deleted: projects table")

def serve():
    server = grpc.aio.server()
    service_pb2_grpc.add_DatabaseServiceServicer_to_server(YourServiceServicer(), server)
    server.add_insecure_port(f"[::]:{server_port}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start())
    loop.run_until_complete(server.wait_for_termination())

if __name__ == "__main__":
    serve()
