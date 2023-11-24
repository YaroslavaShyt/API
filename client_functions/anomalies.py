from utils.imports import anomalies_pb2


async def create_record_anomalies(stub, data):
    response = await stub.CreateAnomaliesRecord(anomalies_pb2.CreateAnomaliesRequest(**data))
    return response


async def read_record_anomalies(stub, data):
    response = await stub.ReadAnomaliesRecord(anomalies_pb2.ReadAnomaliesRequest(**data))
    return response


async def update_record_anomalies(stub, data):
    response = await stub.UpdateAnomaliesRecord(anomalies_pb2.UpdateAnomaliesRequest(**data))
    return response


async def delete_record_anomalies(stub, data):
    response = await stub.DeleteAnomaliesRecord(anomalies_pb2.DeleteAnomaliesRequest(**data))
    return response
