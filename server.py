from utils.servicers_imports import (UsersServicer, ProjectServicer, AnomaliesServicer, LinksServicer)
from utils.imports import load_dotenv, grpc, projects_pb2_grpc, asyncio, users_pb2_grpc, anomalies_pb2, \
    anomalies_pb2_grpc, links_pb2_grpc, links_pb2
from database.connection_params import server_port

load_dotenv()


async def serve() -> None:
    server = grpc.aio.server(options=[
        ('grpc.max_receive_message_length', 100 * 1024 * 1024),  # 100 MB
        ('grpc.max_send_message_length', 100 * 1024 * 1024)  # 100 MB
    ])
    projects_pb2_grpc.add_ProjectsServiceServicer_to_server(
        ProjectServicer(), server)
    users_pb2_grpc.add_UserServiceServicer_to_server(
        UsersServicer(), server)
    anomalies_pb2_grpc.add_AnomaliesServiceServicer_to_server(
        AnomaliesServicer(), server)
    links_pb2_grpc.add_LinksServiceServicer_to_server(
        LinksServicer(), server)
  #  raw_files_pb2_grpc.add_RawFilesServiceServicer_to_server(
  #      RawFilesServicer(), server)
    server.add_insecure_port(f"[::]:{server_port}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
