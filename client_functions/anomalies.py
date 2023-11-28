from utils.imports import anomalies_pb2


async def create_record_anomalies(stub, data):
    response = await stub.CreateRecordAnomalies(anomalies_pb2.CreateAnomaliesRequest(**data))
    return response


async def read_record_anomalies(stub, data):
    response = await stub.ReadRecordAnomalies(anomalies_pb2.ReadAnomaliesRequest(**data))
    return response


async def update_record_anomalies(stub, data):
    response = await stub.UpdateRecordAnomalies(anomalies_pb2.UpdateAnomaliesRequest(**data))
    return response


async def delete_record_anomalies(stub, data):
    response = await stub.DeleteRecordAnomalies(anomalies_pb2.DeleteAnomaliesRequest(**data))
    return response
