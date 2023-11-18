# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto_pb2.raw_files import raw_files_pb2 as proto__pb2_dot_raw__files_dot_raw__files__pb2


class RawFilesServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateRecordRawFiles = channel.unary_unary(
                '/RawFilesService/CreateRecordRawFiles',
                request_serializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.CreateRequestRawFiles.SerializeToString,
                response_deserializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.CreateResponseRawFiles.FromString,
                )
        self.ReadRecordRawFiles = channel.unary_unary(
                '/RawFilesService/ReadRecordRawFiles',
                request_serializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.ReadRequestRawFiles.SerializeToString,
                response_deserializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.ReadResponseRawFiles.FromString,
                )
        self.UpdateRecordRawFiles = channel.unary_unary(
                '/RawFilesService/UpdateRecordRawFiles',
                request_serializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.UpdateRequestRawFiles.SerializeToString,
                response_deserializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.UpdateResponseRawFiles.FromString,
                )
        self.DeleteRecordRawFiles = channel.unary_unary(
                '/RawFilesService/DeleteRecordRawFiles',
                request_serializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.DeleteRequestRawFiles.SerializeToString,
                response_deserializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.DeleteResponseRawFiles.FromString,
                )


class RawFilesServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateRecordRawFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadRecordRawFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateRecordRawFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteRecordRawFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RawFilesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateRecordRawFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateRecordRawFiles,
                    request_deserializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.CreateRequestRawFiles.FromString,
                    response_serializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.CreateResponseRawFiles.SerializeToString,
            ),
            'ReadRecordRawFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.ReadRecordRawFiles,
                    request_deserializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.ReadRequestRawFiles.FromString,
                    response_serializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.ReadResponseRawFiles.SerializeToString,
            ),
            'UpdateRecordRawFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateRecordRawFiles,
                    request_deserializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.UpdateRequestRawFiles.FromString,
                    response_serializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.UpdateResponseRawFiles.SerializeToString,
            ),
            'DeleteRecordRawFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteRecordRawFiles,
                    request_deserializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.DeleteRequestRawFiles.FromString,
                    response_serializer=proto__pb2_dot_raw__files_dot_raw__files__pb2.DeleteResponseRawFiles.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RawFilesService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RawFilesService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateRecordRawFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RawFilesService/CreateRecordRawFiles',
            proto__pb2_dot_raw__files_dot_raw__files__pb2.CreateRequestRawFiles.SerializeToString,
            proto__pb2_dot_raw__files_dot_raw__files__pb2.CreateResponseRawFiles.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReadRecordRawFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RawFilesService/ReadRecordRawFiles',
            proto__pb2_dot_raw__files_dot_raw__files__pb2.ReadRequestRawFiles.SerializeToString,
            proto__pb2_dot_raw__files_dot_raw__files__pb2.ReadResponseRawFiles.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateRecordRawFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RawFilesService/UpdateRecordRawFiles',
            proto__pb2_dot_raw__files_dot_raw__files__pb2.UpdateRequestRawFiles.SerializeToString,
            proto__pb2_dot_raw__files_dot_raw__files__pb2.UpdateResponseRawFiles.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteRecordRawFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RawFilesService/DeleteRecordRawFiles',
            proto__pb2_dot_raw__files_dot_raw__files__pb2.DeleteRequestRawFiles.SerializeToString,
            proto__pb2_dot_raw__files_dot_raw__files__pb2.DeleteResponseRawFiles.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)