from concurrent import futures

import grpc
from google.protobuf import struct_pb2
from google.protobuf.json_format import MessageToDict
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2_grpc

from basegrpc import grpc_pb2
from basegrpc import grpc_pb2_grpc
from basegrpc.grpc_log import grpc_logging
from basegrpc.grpc_module import ml_module
logger = grpc_logging.grpc_log()

class MLServicer(grpc_pb2_grpc.MLServicer):
    def __init__(self):
        self.model_service = ml_module.load_module()
        if self.model_service is None:
            logger.info("Model not loaded!!!!!!")

    def Predict(self, request, context):
        logger.info("Predict: ")
        request = MessageToDict(request).get('request', {})

        logger.info(f"Model input: {request}.")
        model_out = []
        if self.model_service is None:
            logger.info("Model not loaded!!!!!!")
        else:
            model_out = self.model_service.predict(request)
        logger.info(f"Model output: {model_out}.")
        response_data = struct_pb2.Struct()
        response_data.update({"response": model_out})
        return grpc_pb2.MLResponse(response=response_data)


class BaseService:
    def __init__(self):
        self.max_workers = 10
        self.bind_address = "0.0.0.0:50051"

    def run(self):
        try:
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.max_workers))
            grpc_pb2_grpc.add_MLServicer_to_server(MLServicer(), server)

            # health check service - add this service to server
            health_servicer = health.HealthServicer()
            health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

            server.add_insecure_port(self.bind_address)
            server.start()
            logger.info(f"gRPC load module: {ml_module.module_path}")
            logger.info("gRPC server start...")
            server.wait_for_termination()
        except Exception as e:
            logger.info("There was a problem starting gRPC!!!")
            logger.info(f"Error: {e}")
