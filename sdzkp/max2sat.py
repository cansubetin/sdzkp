import random
from itertools import product
from collections import defaultdict
import os

class Max2SAT:
    def __init__(self, num_variables=None, num_clauses=None):
        if num_variables != None:
            self.num_variables = num_variables
        if num_clauses != None:
            self.num_clauses = num_clauses
        self.clauses = set()  # Use a set to store unique clauses
        self.solution = []


    def generate_instance_motoki(self):
        self.solution = [random.choice([True, False]) for _ in range(self.num_variables)]
        #self.solution = [True for _ in range(self.num_variables)]
    
        # Step 1: Choose 4 distinct variables
        distinct_vars = random.sample(range(self.num_variables), 4)
        x_r1, x_r2, x_r3, x_r4 = distinct_vars
        
        # Step 2: Add initial clauses
        self.clauses.add(((x_r1, False), (x_r2, False)))
        self.clauses.add(((x_r3, True), (x_r4, True)))
        
        # Step 3: Add clauses until the formula becomes unsatisfiable
        while self.is_satisfiable(self.clauses):
            x1, x2 = random.sample(range(self.num_variables), 2)
            self.clauses.add(((x1, False), (x2, True)))
        
        # Step 4: Negate literals whose underlying variables are assigned 0 in the optimal assignment
        self.negate_literals()
        self.num_clauses = len(self.clauses)
        self.k = self.check_instance()
        return self.clauses, self.solution
    
    def is_satisfiable(self, formula):
        # Build implication graph
        graph = defaultdict(list)
        reverse_graph = defaultdict(list)
        
        for (x, x_neg), (y, y_neg) in formula:
            graph[(x, not x_neg)].append((y, y_neg))
            graph[(y, not y_neg)].append((x, x_neg))
            reverse_graph[(y, y_neg)].append((x, not x_neg))
            reverse_graph[(x, x_neg)].append((y, not y_neg))
        
        # Kosaraju's algorithm to find SCCs
        def kosaraju_scc(graph, reverse_graph):
            order = []
            visited = set()
            
            def dfs1(node):
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        dfs1(neighbor)
                order.append(node)
            
            def dfs2(node, component):
                visited.add(node)
                component.append(node)
                for neighbor in reverse_graph[node]:
                    if neighbor not in visited:
                        dfs2(neighbor, component)
            
            # First pass
            for node in list(graph.keys()) + list(reverse_graph.keys()):
                if node not in visited:
                    dfs1(node)
            
            # Second pass
            visited.clear()
            components = []
            while order:
                node = order.pop()
                if node not in visited:
                    component = []
                    dfs2(node, component)
                    components.append(component)
            
            return components
        
        sccs = kosaraju_scc(graph, reverse_graph)
        
        # Check if any variable and its negation are in the same SCC
        for component in sccs:
            for index, neg in component:
                if (index, not neg) in component:
                    return False
        
        return True
    
    def negate_literals(self):
        new_clauses = set()
        for clause in self.clauses:
            new_clause = []
            for var, neg in clause:
                if self.solution[var] == False:
                    new_clause.append((var, not neg))
                else:
                    new_clause.append((var, neg))
            new_clauses.add(tuple(new_clause))
        self.clauses = new_clauses
    

    def create_default(self):
        self.num_variables = 3
        self.num_clauses = 4
        self.k = 4
        self.clauses = []
        # Literals are pairs (index, isnegated)
        # x1 V x2
        l1 = (0, False)
        l2 = (1, False)
        clause = tuple([l1, l2])
        self.clauses.append(clause)

        # NOTx1 V x3
        l1 = (0, True)
        l2 = (2, False)
        clause = tuple([l1, l2])
        self.clauses.append(clause)


        # x2 V NOTx3
        l1 = (1, False)
        l2 = (2, True)
        clause = tuple([l1, l2])
        self.clauses.append(clause)


        # NOTx2 V NOTx1
        l1 = (1, True)
        l2 = (0, True)
        clause = tuple([l1, l2])
        self.clauses.append(clause)

        self.solution = [False, True, True]

    def add_clause(self, var1, neg1, var2, neg2):
        clause = tuple(sorted([(var1, neg1), (var2, neg2)]))
        self.clauses.add(clause)
    

    def read_filenames_in_folder(self, folder_path):
        """
        Reads all filenames in the specified folder.

        Args:
        folder_path (str): The path to the folder.

        Returns:
        list: A list of filenames in the folder.
        """
        try:
            filenames = os.listdir(folder_path)
            return filenames
        except Exception as e:
            print(f"An error occurred: {e}")
            return []


    def read_dimacs_file(self,filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        self.num_variables = 0
        self.num_clauses = 0
        self.clauses = set()

        clauses = []
        
        for line in lines:
            if line.startswith('p'):
                parts = line.split()
                self.num_variables = int(parts[2])
                self.num_clauses = int(parts[3])
            elif line.startswith('c') or 'c' in line:
                continue
            elif line.startswith('%') or '%' in line:
                break
            else:
                parts = line.split()
                var1 = int(parts[1])
                var2 = int(parts[2])
                clauses.append((var1, var2))
        
       
        for var1, var2 in clauses:
            neg1 = var1 < 0
            neg2 = var2 < 0
            self.add_clause(abs(var1)-1, neg1, abs(var2)-1, neg2)

    def write_solution_to_file(self, filepath, solution, num_satisfied_clauses):
        """
        Writes the solution and the number of satisfied clauses to a file.

        Args:
        filepath (str): The path to the file where the solution will be written.
        solution (list): The solution assignment for the variables.
        num_satisfied_clauses (int): The number of satisfied clauses.
        """
        try:
            with open(filepath, 'w') as file:
                file.write("Solution:\n")
                file.write(f"{solution}\n")
                file.write("Number of satisfied clauses:\n")
                file.write(f"{num_satisfied_clauses}\n")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    def read_solution_from_file(self, filepath):
        """
        Reads the solution and the number of satisfied clauses from a file.

        Args:
        filepath (str): The path to the file to be read.

        Returns:
        tuple: A tuple containing the solution (list of bool) and the number of satisfied clauses (int).
        """
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
            
            solution_line = lines[1].strip()
            solution = eval(solution_line)  # Convert string representation of list to actual list

            num_satisfied_clauses_line = lines[3].strip()
            num_satisfied_clauses = int(num_satisfied_clauses_line)

            return solution, num_satisfied_clauses
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None, None

    def generate_satisfiable_clause(self, assignment):
        while True:
            var1 = random.randint(1, self.num_variables)
            var2 = random.randint(1, self.num_variables)
            if var1 != var2:
                is_negated1 = not assignment[var1 - 1]
                is_negated2 = not assignment[var2 - 1]
                literal1 = (var1, is_negated1)
                literal2 = (var2, is_negated2)
                clause = tuple(sorted([literal1, literal2]))
                #if clause not in self.clauses:
                #    self.clauses.add(clause)
                return clause


    def generate_unsatisfiable_specific_clause(self, var1, var2, assignment):
        if var1 != var2:
            is_negated1 = assignment[var1 - 1]
            is_negated2 = assignment[var2 - 1]
            literal1 = (var1, is_negated1)
            literal2 = (var2, is_negated2)
            clause = tuple(sorted([literal1, literal2]))
            #if clause not in self.clauses:
            #    self.clauses.add(clause)
            return clause

    def generate_unsatisfiable_clause(self, assignment):
        while True:
            var1 = random.randint(1, self.num_variables)
            var2 = random.randint(1, self.num_variables)
            if var1 != var2:
                is_negated1 = assignment[var1 - 1]
                is_negated2 = assignment[var2 - 1]
                literal1 = (var1, is_negated1)
                literal2 = (var2, is_negated2)
                clause = tuple(sorted([literal1, literal2]))
                #if clause not in self.clauses:
                #    self.clauses.add(clause)
                return clause

    def is_clause_satisfied(self, clause, assignment):
        lit1, lit2 = clause
        var1, is_negated1 = lit1
        var2, is_negated2 = lit2
        val1 = not assignment[var1 ] if is_negated1 else assignment[var1 ]
        val2 = not assignment[var2 ] if is_negated2 else assignment[var2 ]
        return val1 or val2

    def check_instance(self, solution=None):
        if solution == None:
            solution = self.solution
        satisfied_clauses_count = 0
        for clause in self.clauses:
            if self.is_clause_satisfied(clause, solution):
                satisfied_clauses_count += 1
        return satisfied_clauses_count

    def print_clause(self, clause):
    
        lit1, lit2 = clause
        lit1_str = f"¬x{lit1[0]}" if lit1[1] else f"x{lit1[0]}"
        lit2_str = f"¬x{lit2[0]}" if lit2[1] else f"x{lit2[0]}"
        print(f"({lit1_str} ∨ {lit2_str})")
        
    def print_instance(self):
        for clause in self.clauses:
            lit1, lit2 = clause
            lit1_str = f"¬x{lit1[0]}" if lit1[1] else f"x{lit1[0]}"
            lit2_str = f"¬x{lit2[0]}" if lit2[1] else f"x{lit2[0]}"
            #print(f"({lit1_str} ∨ {lit2_str})")
        #print("Solution ", self.solution)
    
    def solve(self):
        assignment = [random.choice([True, False]) for _ in range(self.num_variables)]
        for var in range(0, self.num_variables):
            true_assignment = assignment.copy()
            true_assignment[var ] = True
            false_assignment = assignment.copy()
            false_assignment[var ] = False

            true_count = self.check_instance(solution=true_assignment)
            false_count = self.check_instance(solution=false_assignment)

            if true_count < false_count:
                assignment[var ] = True
            else:
                assignment[var ] = False
        self.k = self.check_instance(assignment)
        self.solution = assignment
        return assignment, self.k

  
    def enumerate_all_assignments(self):
        max_satisfied = 0
        best_assignment = []
        
        for assignment in product([True, False], repeat=self.num_variables):
            satisfied_count = self.check_instance(assignment)
            #print(f"Assignment: {assignment}, Satisfied Clauses: {satisfied_count}")
            
            if satisfied_count > max_satisfied:
                best_assignment.clear()
                max_satisfied = satisfied_count
                best_assignment.append(assignment)
            if satisfied_count == max_satisfied:
                best_assignment.append(assignment)

        print("Check if solution in best assignments ", tuple(self.solution) in best_assignment)
        for t in best_assignment:
            print(f"tuple: {t}, k: {max_satisfied}, check {self.check_instance(t)}")
        return best_assignment, max_satisfied