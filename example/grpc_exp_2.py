from basegrpc.grpc_service import BaseService, logger
import json


class CustomGrpc(BaseService):
    def __init__(self):
        super().__init__()
        self.parameters = self.load_parameters()
        self.max_workers = self.parameters["max_workers"]
        self.bind_address = self.parameters["bind_address"]

    def load_parameters(self) -> dict:
        with open("env.json", "r") as f:
            env = json.load(f)
        parameters = {}
        project_name = env.get("projectName", "")
        environment = env.get("environment", "")
        host = env.get("grpc", {}).get("server", {}).get("serviceHost", "0.0.0.0")
        port = env.get("grpc", {}).get("server", {}).get("port", "50051")
        parameters["bind_address"] = host + ":" + port
        parameters["max_workers"] = env.get("grpc", {}).get("server", {}).get("maxWorkers", 10)

        logger.info(f"projectName: {project_name}")
        logger.info(f"environment: {environment}")
        return parameters


if __name__ == '__main__':
    grpc_service = CustomGrpc()
    grpc_service.run()

# output:
# [PID 1268] projectName: Test-1
# [PID 1268] environment: staging
# [PID 1268] gRPC load module: Logic
# [PID 1268] gRPC server start...
