from utils.imports import service_pb2_grpc
from utils.servicers_imports import ProjectServicer, LinksServicer, MemberPermissionsServicer, ProjectPermissionsSettingsServicer, ProjectMembersServicer, RawFilesServicer, AnomaliesServicer, ProcessedFilesServicer


class APIServicer(service_pb2_grpc.DatabaseServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.servicers = {
            "PROJECTS": ProjectServicer(),
            "LINKS": LinksServicer(),
            "MEMBER_PERMISSIONS": MemberPermissionsServicer(),
            "PROJECT_PERMISSIONS_SETTINGS" : ProjectPermissionsSettingsServicer(),
            "PROJECT_MEMBERS": ProjectMembersServicer(),
            "RAW_FILES": RawFilesServicer(),
            "ANOMALIES": AnomaliesServicer(),
            "PROCESSED_FILES" : ProcessedFilesServicer()
        }
