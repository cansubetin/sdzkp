import timeit
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sdzkp.max2sat import Max2SAT
from sdzkp.sgd import SubgroupDistanceProblemWithSolution

def benchmark_sgd_instance_generation(num_variables):
    max2satinstance = Max2SAT(num_variables=num_variables)
    max2satinstance.generate_instance_motoki()
    sgd = SubgroupDistanceProblemWithSolution(max2satinstance)

# Values of num_variables to test
generator_sizes = range(8,64,8) #[16, 32, 64, 128, 256, 512, 1024]

# Store the execution times
execution_means = []
execution_cis = []

# Benchmark for each value of num_variables
for num_generators in generator_sizes:
    # Measure the execution time for the given num_variables multiple times
    num_variables = round(num_generators/2)
    times = timeit.repeat(lambda: benchmark_sgd_instance_generation(num_variables), repeat=100, number=1)
    
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
plt.title('SGD Instance Generation Time with 95% Confidence Interval')
plt.xlabel('Number of Generators')
plt.ylabel('Execution Time (seconds)')
plt.grid(True)
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig('docs/figures/sgd_benchmark_with_ci.png')

# Optionally, display the plot
plt.show()
