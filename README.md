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
* Model file: `/examples/logic.mdl`
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
from basegrpc.grpc_client import GrpcClient


if __name__ == "__main__":
    grpc_client = GrpcClient(bind_address='127.0.0.1:50051')
    data = {"data_X": [[5.1, 3.5]]}
    response = grpc_client.request(request_data=data)
    print("response: ", response)

    health_status = grpc_client.health_check()
    print("health status: ", health_status)
    
# output:
# [0.0]
# status: SERVING

```
