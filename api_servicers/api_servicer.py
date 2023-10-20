from utils.imports import service_pb2, service_pb2_grpc, MessageToDict, Struct, sessionmaker
from database.engine import engine
from database.tables import projects


Session = sessionmaker(bind=engine)


class APIServicer(service_pb2_grpc.DatabaseServiceServicer):
    def CreateRecord(self, request, context):
        data_dict = MessageToDict(request.data)
        session = Session()
        new_record = projects.insert().values(
            name=data_dict["name"], description=data_dict["description"], status=data_dict["status"])
        session.execute(new_record)
        session.commit()
        session.close()
        struct = Struct()
        struct.update({"success": True})
        return service_pb2.CreateResponse(data=struct)


    def ReadRecord(self, request, context):
        data_dict = MessageToDict(request.data)
        print(f'\n\n{data_dict}\n\n')
        session = Session()
        record = projects.select().where(projects.c.id == int(data_dict["id"]))
        print(f'\n\n{record}\n\n')
        result = session.execute(record).fetchone()
        print(
            f'\n\n{result[0]} {result[1]} {result[2]} {result[3]} {result[4]}\n\n')
        session.close()
        if result:
            print('in result')
            data = {
                "success": True,
                "id": result[0],
                "name": result[1],
                "description": result[2],
                "timestamp": str(result[3]),
                "status": result[4]}
        else:
            data = {"success": False}
        print('before struct')
        struct = Struct()
        struct.update(data)
        print(f'\n\nstruct {struct}')
        return service_pb2.CreateResponse(data=struct)


    def UpdateRecord(self, request, context):
        data_dict = MessageToDict(request.data)
        session = Session()
        update_query = projects.update().where(projects.c.id == data_dict["id"]).values(
            name=data_dict["name"], description=data_dict["description"], status=data_dict["status"])
        session.execute(update_query)
        session.commit()
        session.close()
        struct = Struct()
        struct.update({"success": True})
        return service_pb2.UpdateResponse(data=struct)


    def DeleteRecord(self, request, context):
        data_dict = MessageToDict(request.data)
        session = Session()
        delete_query = projects.delete().where(
            projects.c.id == data_dict["id"])
        session.execute(delete_query)
        session.commit()
        session.close()
        struct = Struct()
        struct.update({"success": True})
        return service_pb2.UpdateResponse(data=struct)