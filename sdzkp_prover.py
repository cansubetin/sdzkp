# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC sdzkp.Greeter client."""

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
