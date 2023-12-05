from utils.imports import links_pb2, sessionmaker
from database.engine import engine
from database.tables import projects, links
from utils.check_input_functions import *

Session = sessionmaker(bind=engine)


class LinksServicer(anomalies_pb2_grpc.AnomaliesServiceServicer):
    def __init__(self):
        # define field types for better check-outs
        self.required_fields    = ['projectId', 'token', 'status']
        self.string_fields      = ['token']
        self.integer_fields     = ['projectId', 'status']
        self.other_table_values = {projects: None}

    def CreateRecordLinks(self, request, context):
        try:
            # check required fields
            success, field_name = check_required_fields(request, self.required_fields)
            if not success:
                data = {"success": success, "message": [
                    f'Error: <{field_name}> is required but not provided.']}
                return links_pb2.CreateLinksResponse(**data)

            # check if string fields are not empty
            success, field_name = check_string_fields(request, self.string_fields)
            if not success:
                data = {"success": success, "message": [f'Error: <{field_name}> cannot be empty or include whitespaces only.']}
                return links_pb2.CreateLinksResponse(**data)

            # check if value in allowed range
            success, field_name = check_integer_in_range(request.status, (0, 1))
            if not success:
                data = {"success": False, "message": [f'Error: <status> cannot be {request.status}. Only allowed values - 0 or 1']}
                return links_pb2.CreateLinksResponse(**data)

            with Session() as session:
                # check projectId exists
                self.other_table_values[projects] = request.projectId
                success, field_name, = check_id_in_table(session, self.other_table_values)
                if not success:
                    if field_name == projects:
                        field_name = 'projectsId'
                    field_value = getattr(request, field_name, None)
                    data = {"success": success, "message": [
                        f"No matching records found for {field_name} <{field_value}>."]}
                    return links_pb2.CreateLinksResponse(**data)

                # do database query
                new_record = links.insert().values(
                    projectId=request.projectId,
                    token=request.token,
                    status=request.status
                )
                session.execute(new_record)
                session.commit()
                result = {"success": True, "message": ["Record created"]}
        except Exception as e:
            result = {"success": False, "message": [str(e)]}
        return links_pb2.CreateLinksResponse(**result)



    def ReadRecordLinks(self, request, context):
        try:
            pass
        except ex:
            pass

    def UpdateRecordLinks(self, request, context):
        try:
            pass
        except ex:
            pass

    def DeleteRecordLinks(self, request, context):
        try:
            pass
        except ex:
            pass