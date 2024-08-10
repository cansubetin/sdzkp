
"""A simple Python code to showcase prover."""

from __future__ import print_function

import logging

import grpc
from sdzkp.sdzkproto import sdzkp_pb2
from sdzkp.sdzkproto import sdzkp_pb2_grpc
from sdzkp.prover import Prover
import uuid


import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))


def run():
    
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = sdzkp_pb2_grpc.SDZKPStub(channel)
        alice = Prover(stub, uuid.uuid4(), 100, 16)
        alice.run()
#      challengemessage = stub.Commit(sdzkp_pb2.Commitments(sgdid="3", commitment="commitments"))
#    print("Received: " , challengemessage.sgdid, challengemessage.challenge)


if __name__ == "__main__":
    logging.basicConfig()
    run()
