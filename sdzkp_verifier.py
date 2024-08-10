"""The Python implementation of the SDZKP."""

from concurrent import futures
import logging

import grpc


from sdzkp.sdzkproto import sdzkp_pb2
from sdzkp.sdzkproto import sdzkp_pb2_grpc
from sdzkp.verifier import Verifier


class SDZKP(sdzkp_pb2_grpc.SDZKPServicer):

    def __init__(self) -> None:
        super().__init__()
        self.verifiers = {}

    def Setup(self, request, context):
        self.verifiers[request.sgdid] = Verifier(request.sgdid)
        return self.verifiers[request.sgdid].handleSetup(request)
    
    def Commit(self, request, context):
        return self.verifiers[request.sgdid].handleCommit(request)

    def Verify(self, request, context):
        return self.verifiers[request.sgdid].handleVerify(request)


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sdzkp_pb2_grpc.add_SDZKPServicer_to_server(SDZKP(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
