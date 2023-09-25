from basegrpc.grpc_service import BaseService
from basegrpc.grpc_module import ml_module
import glob


def find_module_path(module_name="LogicV1"):
    module_paths = [file.replace("\\", ".").replace("/", ".").replace(".py", "") for file in
                    glob.glob('**/*.py', recursive=True)]
    if module_name == "":
        matches = ['grpc', 'test', '__init__', 'setup']
        for module_path in module_paths:
            if not any(x in module_path for x in matches):
                return module_path
    else:
        for module_path in module_paths:
            if module_name in module_path:
                return module_path

def run():
    ml_module.find_module_path = find_module_path
    grpc_service = BaseService()
    grpc_service.run()


if __name__ == '__main__':
    run()

# output:
# [PID 7640] gRPC load module: LogicV1
# [PID 7640] gRPC server start...
