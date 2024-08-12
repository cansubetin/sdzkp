
"""A simple Python code to showcase prover."""
from __future__ import print_function

import logging

import grpc
from sdzkp.sdzkproto import sdzkp_pb2
from sdzkp.sdzkproto import sdzkp_pb2_grpc
from sdzkp.prover import Prover
import uuid
MAX_MESSAGE_LENGTH = 1024*1024*1024
def run():
    
    with grpc.insecure_channel("localhost:50051", options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
    ], compression=grpc.Compression.Gzip) as channel:
        stub = sdzkp_pb2_grpc.SDZKPStub(channel)
        alice = Prover(stub, uuid.uuid4(), 5, 16)
        alice.run()


if __name__ == "__main__":
    logging.basicConfig()
    run()

