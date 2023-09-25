from basegrpc.grpc_client import GrpcClient


if __name__ == "__main__":
    grpc_client = GrpcClient(bind_address='127.0.0.1:50051')
    data = {"data_X": [[5.1, 3.5]]}
    response = grpc_client.request(request_data=data)
    print("response: ", response)

    health_status = grpc_client.health_check()
    print("health status: ", health_status)

# output:
# response:  [0.0]
# health status:  status: SERVING
