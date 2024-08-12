import random
from itertools import product
from collections import defaultdict
import os

class Max2SAT:
    """
    A class to represent and manipulate instances of the MAX2SAT problem.
    MAX2SAT is a special case of the Boolean satisfiability problem where each clause
    contains exactly two literals. The objective is to determine the maximum number of clauses 
    that can be satisfied by some assignment of truth values to the variables.
    """
    
    def __init__(self, num_variables=None, num_clauses=None):
        """
        Initializes a new instance of the Max2SAT class.
        
        Parameters:
            num_variables (int): Number of variables in the problem instance.
            num_clauses (int): Number of clauses in the problem instance.
        """
        if num_variables is not None:
            self.num_variables = num_variables
        if num_clauses is not None:
            self.num_clauses = num_clauses
        self.clauses = set()  # Store unique clauses using a set
        self.solution = []    # Solution vector (truth assignment to variables)
    
    def generate_instance_motoki(self):
        """
        Generates a random MAX2SAT instance using a method inspired by Motoki's approach.
        
        This method randomly assigns truth values to each variable and generates clauses
        based on these assignments.
        """
        # Randomly assign True/False to each variable
        self.solution = [random.choice([True, False]) for _ in range(self.num_variables)]
        while len(self.clauses) < self.num_clauses:
            # Randomly select two distinct variables
            var1, var2 = random.sample(range(1, self.num_variables + 1), 2)
            # Randomly assign negations
            lit1 = var1 if random.choice([True, False]) else -var1
            lit2 = var2 if random.choice([True, False]) else -var2
            # Add the clause (lit1 OR lit2) to the set of clauses
            self.clauses.add((lit1, lit2))

    # Add more methods and their documentation as necessary...

