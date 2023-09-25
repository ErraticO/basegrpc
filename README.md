# Base gRPC

[![PyPI version](https://badge.fury.io/py/rankfm.svg)](https://github.com/ErraticO/basegrpc)
[![CircleCI](https://circleci.com/gh/etlundquist/rankfm.svg?style=shield)](https://github.com/ErraticO/basegrpc)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

It is a universal gRPC service framework suitable for model as a service.
The data is input-output like JSON.
Different services only need to add different model class files.
At the same time, extension also becomes easy, as it can be inherited or replaced.

* see the **Quickstart** section below to get started with the basic functionality
* see the `/examples` folder for more in-depth `py` walkthroughs

---
### Dependencies
* grpcio >= 1.57.0
* grpcio_health_checking >= 1.56.0
* protobuf >= 4.24.3
* scikit_learn >= 1.2.1

### Installation

#### Package Installation

You can install the latest published version from PyPI using `pip`:
```
pip install basegrpc
```

### Quickstart
#### Prerequisites
* Input / output: please refer to the [struct](https://github.com/protocolbuffers/protobuf/blob/main/src/google/protobuf/struct.proto) of gRPC
* Model file: `/examples/logic.mdl`(It can be placed in any directory of the project)
* Model class files: the file name and class name must be the same(`Logic.py` and `class Logic`)
```python
import pickle
import numpy as np


class Logic(object):
    def __init__(self):
        self.model_path = "logic.mdl"
        # load model
        self.model = self.load_model()

    def load_model(self):
        with open(self.model_path, "rb") as pickle_file:
            model = pickle.load(pickle_file)
        return model

    def predict(self, data) -> list:
        result = np.array([])
        try:
            data_X = data['data_X']
            result = self.model.predict(data_X)
        except Exception as e:
            print(e)
        return result.tolist()
```

#### Start Service
```python
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
```
#### Test
```python
from basegrpc import grpc_pb2, grpc_pb2_grpc
import grpc
import time
from grpc_health.v1 import health_pb2_grpc
from grpc_health.v1 import health_pb2
from google.protobuf import struct_pb2
from google.protobuf.json_format import MessageToDict


def run(request):
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = grpc_pb2_grpc.MLStub(channel)

    request_data = struct_pb2.Struct()
    request_data.update(request)

    response = stub.Predict(grpc_pb2.MLRequest(request=request_data))
    response = MessageToDict(response)
    print(f"{response['response']['response']}")

    health_stub = health_pb2_grpc.HealthStub(channel)
    health_response = health_stub.Check(health_pb2.HealthCheckRequest())
    print(f"{health_response}")


if __name__ == "__main__":
    start = time.time()
    run({"data_X": [[5.1, 3.5]]})
    print(time.time()-start)
    
# output:
# [0.0]
# status: SERVING
# 
# 0.01999950408935547
```
