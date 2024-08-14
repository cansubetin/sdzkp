
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
num_generators = 8
num_variables = round(num_generators/2)
round_sizes = range (1,30,1)
num_repeat = 1000
cheating_prob = []


def benchmark_honest_prover(stub, num_rounds, num_variables):
    alice = DishonestProver(stub, uuid.uuid4(), num_rounds, num_variables)
    rr, zkpr = alice.run()
    num_trues = sum(rr)
    if num_trues==num_rounds:
        prob = 1
    else:
        prob = 0
    #print(prob)
    cheating_prob.append(prob)
    

def run():

    # Store the execution times
    execution_means = []
    execution_cis = []

    execution_prob_means = []
    execution_prob_cis = []

    with grpc.insecure_channel("localhost:50051", options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
    ], compression=grpc.Compression.Gzip) as channel:
        stub = sdzkp_pb2_grpc.SDZKPStub(channel)

        # Benchmark for each value of num_variables
        for num_rounds in round_sizes:
            # Measure the execution time for the given num_variables multiple times
            cheating_prob.clear()
            times = timeit.repeat(lambda: benchmark_honest_prover(stub, num_rounds, num_variables), repeat=num_repeat, number=1)
            
            # Calculate mean and 95% confidence interval
            mean_time = np.mean(times)
            ci = stats.sem(times) * stats.t.ppf((1 + 0.95) / 2, len(times) - 1)
            
            execution_means.append(mean_time)
            execution_cis.append(ci)
            
            print(f"Execution time for num_generators={num_generators}: {mean_time:.5f} seconds (±{ci:.5f} seconds)")
            probs = np.array(cheating_prob)
            mean_prob = np.mean(probs)
            ci_prob = stats.sem(probs) * stats.t.ppf((1 + 0.95) / 2, len(probs) - 1)
            
            execution_prob_means.append(mean_prob)
            execution_prob_cis.append(ci_prob)
            print(f"Cheating prob for num_rounds={num_rounds}: {mean_prob:.5f}  (±{ci_prob:.5f} )")
        
    # Convert lists to numpy arrays for easier plotting
    execution_means = np.array(execution_means)
    execution_cis = np.array(execution_cis)

    execution_prob_means = np.array(execution_prob_means)
    execution_prob_cis = np.array(execution_prob_cis)


    # # Plotting the results
    # plt.figure(figsize=(10, 6))
    # plt.errorbar(generator_sizes, execution_means, yerr=execution_cis, fmt='o-', capsize=5, capthick=2)
    # plt.title('Dihonest Prover Execution Time for Soundness with 95% Confidence Interval')
    # plt.xlabel('Number of Generators')
    # plt.ylabel('Execution Time (seconds)')
    # plt.grid(True)

    # # Save the figure as a PNG file
    # plt.savefig('docs/figures/soundness_executiontime_with_ci.png')

    # Optionally, display the plot
    # plt.show()

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.errorbar(round_sizes, execution_prob_means, yerr=execution_prob_cis, fmt='o-', capsize=5, capthick=2)
    plt.title('Cheating Probability for Soundness ')
    plt.xlabel('Number of Rounds')
    plt.ylabel('Cheating Probability')
    plt.grid(True)

    # Save the figure as a PNG file
    plt.savefig('docs/figures/soundness_cheating_prob.png')

    plt.show()

if __name__ == "__main__":
    logging.basicConfig()
    run()
    