from basegrpc.grpc_service import BaseService
from basegrpc.grpc_module import ml_module


def run():
    ml_module.module_name = "LogicV1"
    grpc_service = BaseService()
    grpc_service.run()


if __name__ == '__main__':
    run()

# output:
# [PID 11732] gRPC load module: LogicV1
# [PID 11732] gRPC server start...
