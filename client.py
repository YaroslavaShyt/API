import grpc
import service_pb2
import service_pb2_grpc

def create_record(stub, name, description, status):
    response = stub.CreateRecord(service_pb2.CreateRequest(name=name, description=description, status=status))
    return response.message

def read_record(stub, record_id):
    response = stub.ReadRecord(service_pb2.ReadRequest(record_id=record_id))
    if response.data:
        return response.data
    else:
        return response.data

def update_record(stub, record_id, name, description, status):
    response = stub.UpdateRecord(service_pb2.UpdateRequest(record_id=record_id, name=name, description=description, status=status))
    return response.message

def delete_record(stub, record_id):
    response = stub.DeleteRecord(service_pb2.DeleteRequest(record_id=record_id))
    return response.message

def main():
   
    channel = grpc.insecure_channel("localhost:50051")
    stub = service_pb2_grpc.DatabaseServiceStub(channel)

   
    record_id = create_record(stub, "project 1", "test project 1", "active")
    print(f"Created record with ID {record_id}")

    record = read_record(stub, record_id)
    print(f"Read record: {record}")

    update_result = update_record(stub, record_id, "newuser", "new@example.com", "newpassword")
    print(f"Update result: {update_result}")

    delete_result = delete_record(stub, record_id)
    print(f"Delete result: {delete_result}")

if __name__ == "__main__":
    main()

