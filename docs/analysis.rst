====================
Performance Analysis
====================


Trusted Setup Related Tasks
===========================

In this section, we present the performance evaluation results for NP problem instance generation. The subgroup distance problem (SGD) 
relies on Max2SAT instances. We firstly create a Max2SAT instance using Motoki's algorithm. Then we convert the Max2SAT instance to SGD instance
using our novel approach.

Max2SAT Instance Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For Max2SAT instance generation we use Motoki's approach: Mitsuo Motoki , "Test Instance Generation for MAX 2SAT with Fixed Optimal Value", Japan Advanced Institute of Science and Technology, School of Information Science

The paper proposes a randomized algorithm to generate test instances for the MAX 2SAT problem. The algorithm ensures that the generated instances have exactly one unsatisfied clause at the optimal solution, with a probability of 1. The author proves that the number of clauses in the generated instances is, with high probability, greater than the number of variables, aligning with known thresholds for unsatisfiability in random 2CNF formulas.

MAX 2SAT is a well-known NP-complete combinatorial optimization problem, where the goal is to find a truth assignment that maximizes the number of satisfied clauses in a 2CNF formula. To evaluate the performance of approximation algorithms for MAX 2SAT, both theoretical analysis and empirical studies are used. However, empirical studies require test instances with known optimal solutions. The paper addresses the challenge of generating such instances randomly.

The proposed algorithm generates an instance by first selecting a truth assignment `t` as the optimal solution. It then adds one randomly chosen clause that is unsatisfied by `t` and continues to add clauses satisfied by `t` until the formula becomes unsatisfiable. The algorithm ensures that the generated instance has a fixed optimal value, specifically one unsatisfied clause.

The paper analyzes the number of clauses added until the algorithm halts. It demonstrates that the threshold for the number of clauses is the number of variables, meaning that the algorithm is likely to stop only when the number of clauses exceeds the number of variables. This result coincides with the threshold for unsatisfiability in 2CNF formulas. The paper also provides a detailed mathematical analysis, proving that the algorithm works with high probability.

The paper presents a significant contribution to the generation of test instances for MAX 2SAT, providing a useful tool for evaluating approximation algorithms. The approach is mathematically rigorous and ensures that the generated instances meet the desired criteria with high probability.


.. _fig-max2sat_benchmark_with_ci:

.. figure:: figures/max2sat_benchmark_with_ci.png
   :alt:  The execution times with 95% confidence for Max2SAT problem instance generation.

   The execution times with 95% confidence for Max2SAT problem instance generation.


:numref:`fig-max2sat_benchmark_with_ci` illustrates the execution time required to generate a `Max2SAT` instance as a function 
of the number of variables. The data points are plotted with error bars that represent the 95% confidence intervals, providing 
a visual indication of the variability in the measurements. As the number of variables increases, the execution time also 
increases. This is consistent with the expected behavior as more complex instances with larger numbers of variables require 
more computational resources to generate. The error bars show that the variability in execution time also increases with 
the number of variables, which is typical as the system may experience greater fluctuations in processing time due to 
the increased complexity of the problem instances. Overall, the figure effectively conveys the relationship between 
the number of variables in a `Max2SAT` instance and the time required to generate it, highlighting both the trend and 
the associated uncertainties.


Subgroup Distance Problem Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. _fig-sgd_benchmark_with_ci:

.. figure:: figures/sgd_benchmark_with_ci.png
   :alt:  The execution times with 95% confidence for SGD problem instance generation.

   The execution times with 95% confidence for SGD problem instance generation.
