# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\x12\x05myapp\x1a\x1cgoogle/protobuf/struct.proto\"6\n\rCreateRequest\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"7\n\x0e\x43reateResponse\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"4\n\x0bReadRequest\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"5\n\x0cReadResponse\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"6\n\rUpdateRequest\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"7\n\x0eUpdateResponse\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"6\n\rDeleteRequest\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"7\n\x0e\x44\x65leteResponse\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct2\xff\x01\n\x0f\x44\x61tabaseService\x12;\n\x0c\x43reateRecord\x12\x14.myapp.CreateRequest\x1a\x15.myapp.CreateResponse\x12\x35\n\nReadRecord\x12\x12.myapp.ReadRequest\x1a\x13.myapp.ReadResponse\x12;\n\x0cUpdateRecord\x12\x14.myapp.UpdateRequest\x1a\x15.myapp.UpdateResponse\x12;\n\x0c\x44\x65leteRecord\x12\x14.myapp.DeleteRequest\x1a\x15.myapp.DeleteResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CREATEREQUEST._serialized_start=54
  _CREATEREQUEST._serialized_end=108
  _CREATERESPONSE._serialized_start=110
  _CREATERESPONSE._serialized_end=165
  _READREQUEST._serialized_start=167
  _READREQUEST._serialized_end=219
  _READRESPONSE._serialized_start=221
  _READRESPONSE._serialized_end=274
  _UPDATEREQUEST._serialized_start=276
  _UPDATEREQUEST._serialized_end=330
  _UPDATERESPONSE._serialized_start=332
  _UPDATERESPONSE._serialized_end=387
  _DELETEREQUEST._serialized_start=389
  _DELETEREQUEST._serialized_end=443
  _DELETERESPONSE._serialized_start=445
  _DELETERESPONSE._serialized_end=500
  _DATABASESERVICE._serialized_start=503
  _DATABASESERVICE._serialized_end=758
# @@protoc_insertion_point(module_scope)
