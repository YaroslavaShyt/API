from utils.imports import service_pb2, service_pb2_grpc, sessionmaker
from database.engine import engine
from database.tables import projects


Session = sessionmaker(bind=engine)


class APIServicer(service_pb2_grpc.DatabaseServiceServicer):

    def CreateRecord(self, request, context):
        with Session() as session:
            new_record = projects.insert().values(
                name=request.name, description=request.description, status=request.status)
            session.execute(new_record)
            session.commit()
            session.close()
        result = {"success": True, "message": "Record created"}
        return service_pb2.CreateResponse(**result)

    def ReadRecord(self, request, context):
        with Session() as session:
            record = projects.select().where(
                projects.c.id == request.id)
            result = session.execute(record).fetchone()
            session.close()
        if result:
            data = {
                "success": True,
                "id": result[0],
                "name": result[1],
                "description": result[2],
                "timestamp": str(result[3]),
                "status": result[4]}
        else:
            data = {"success": False}
        return service_pb2.ReadResponse(**data)

    def UpdateRecord(self, request, context):
        with Session() as session:
            update_query = projects.update().where(projects.c.id == request.id).values(
                name=request.name, description=request.description, status=request.status)
            session.execute(update_query)
            session.commit()
            session.close()
        result = {"success": True, "message": "Record updated"}
        return service_pb2.UpdateResponse(**result)

    def DeleteRecord(self, request, context):
        with Session() as session:
            delete_query = projects.delete().where(
                projects.c.id == request.id)
            session.execute(delete_query)
            session.commit()
            session.close()
        result = {"success": True, "message": "Record updated"}
        return service_pb2.UpdateResponse(**result)
