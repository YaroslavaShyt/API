from utils.imports import load_dotenv, grpc, service_pb2_grpc, asyncio
from database.connection_params import server_port
from server_functions.api_servicer import APIServicer


load_dotenv()


async def serve() -> None:
    server = grpc.aio.server()
    service_pb2_grpc.add_DatabaseServiceServicer_to_server(
        APIServicer(), server)
    server.add_insecure_port(f"[::]:{server_port}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
