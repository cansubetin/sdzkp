
"""A simple Python code to showcase honest prover and the completeness of SDZKP."""
from __future__ import print_function

import logging

import grpc
from sdzkp.sdzkproto import sdzkp_pb2
from sdzkp.sdzkproto import sdzkp_pb2_grpc
from sdzkp.prover import Prover, DishonestProver, HonestProver
import uuid
import timeit
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import sys


MAX_MESSAGE_LENGTH = 1024*1024*1024


# Values of num_variables to test
generator_sizes = range(8,24,2) #[16, 32, 64, 128, 256, 512, 1024]
num_rounds = 100



def benchmark_honest_prover(stub, num_rounds, num_variables):
    alice = HonestProver(stub, uuid.uuid4(), num_rounds, num_variables)
    rr, zkpr = alice.run()
    if all(rr):
        #print("All rounds are True")
        pass
    else:
        print("Completeness Failed!")
        sys.exit("Completeness Test Failed!")


def run():

    # Store the execution times
    execution_means = []
    execution_cis = []

    with grpc.insecure_channel("localhost:50051", options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
    ], compression=grpc.Compression.Gzip) as channel:
        stub = sdzkp_pb2_grpc.SDZKPStub(channel)

        # Benchmark for each value of num_variables
        for num_generators in generator_sizes:
            # Measure the execution time for the given num_variables multiple times
            num_variables = round(num_generators/2)
            times = timeit.repeat(lambda: benchmark_honest_prover(stub, num_rounds, num_variables), repeat=100, number=1)
            
            # Calculate mean and 95% confidence interval
            mean_time = np.mean(times)
            ci = stats.sem(times) * stats.t.ppf((1 + 0.95) / 2, len(times) - 1)
            
            execution_means.append(mean_time)
            execution_cis.append(ci)
            
            print(f"Execution time for num_generators={num_generators}: {mean_time:.5f} seconds (±{ci:.5f} seconds)")

        
    # Convert lists to numpy arrays for easier plotting
    execution_means = np.array(execution_means)
    execution_cis = np.array(execution_cis)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.errorbar(generator_sizes, execution_means, yerr=execution_cis, fmt='o-', capsize=5, capthick=2)
    plt.title('Honest Prover Execution Time for Completeness with 95% Confidence Interval')
    plt.xlabel('Number of Generators')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True)

    # Save the figure as a PNG file
    plt.savefig('docs/figures/completeness_with_ci.png')

    # Optionally, display the plot
    plt.show()


if __name__ == "__main__":
    logging.basicConfig()
    run()

