import timeit
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sdzkp.max2sat import Max2SAT
from sdzkp.sgd import SubgroupDistanceProblemWithSolution
import random
from sdzkp.sdzkproto import sdzkp_pb2
from sdzkp.verifier import Verifier

max2satinstance = None
sgd = None

def benchmark_verifier_verification(verifier, responsemessage):
    #res = 
    verifier.handleVerify(responsemessage)
    #print(res)
    

# Values of num_variables to test
generator_sizes = range(8,128,8) #[16, 32, 64, 128, 256, 512, 1024]

# Store the execution times
execution_means = []
execution_cis = []

# Benchmark for each value of num_variables
for num_generators in generator_sizes:
    # Measure the execution time for the given num_variables multiple times
    num_variables = round(num_generators/2)
    max2satinstance = Max2SAT(num_variables=num_variables)
    max2satinstance.generate_instance_motoki()
    sgd = SubgroupDistanceProblemWithSolution(max2satinstance)
    rd = sgd.setup_sdzkp_round(1)
    c = random.randint(0, 2)
    instance_id = "1"
    match c:
        case 0:
            responsemessage = sdzkp_pb2.Response(
                sgdid=instance_id,
                roundid=1,
                Z1=rd.Z1,
                s=rd.s,
                t_u=rd.t_u
            )
        case 1:
            responsemessage = sdzkp_pb2.Response(
                sgdid=instance_id,
                roundid=1,
                Z2=rd.Z2,
                s=rd.s,
                t_r=rd.t_r
            )
        case 2:
            responsemessage = sdzkp_pb2.Response(
                sgdid=instance_id,
                roundid=1,
                Z1=rd.Z1,
                Z2=rd.Z2
            )
        case _:
            print("Error in challenge, abort")
    verifier = Verifier(instance_id)
    verifier.SGD = sgd
    verifier.rd = rd
    times = timeit.repeat(lambda: benchmark_verifier_verification(verifier, responsemessage), repeat=100, number=1)
    
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
plt.title('Verification Time by the Verifier with 95% Confidence Interval')
plt.xlabel('Number of Generators')
plt.ylabel('Execution Time (seconds)')
plt.grid(True)
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig('docs/figures/verifier_verification_with_ci.png')

# Optionally, display the plot
plt.show()
