from basegrpc import grpc_pb2, grpc_pb2_grpc
import grpc
from grpc_health.v1 import health_pb2_grpc
from grpc_health.v1 import health_pb2
from google.protobuf import struct_pb2
from google.protobuf.json_format import MessageToDict

class GrpcClient:
    def __init__(self, bind_address):
        self.bind_address = bind_address
        self.channel = grpc.insecure_channel(self.bind_address)

    def request(self, request_data):
        request_struct = struct_pb2.Struct()
        request_struct.update(request_data)

        stub = grpc_pb2_grpc.MLStub(self.channel)
        response = stub.Predict(grpc_pb2.MLRequest(request=request_struct))
        response = MessageToDict(response)
        return response['response']['response']

    def health_check(self):
        health_stub = health_pb2_grpc.HealthStub(self.channel)
        health_response = health_stub.Check(health_pb2.HealthCheckRequest())
        return health_response

