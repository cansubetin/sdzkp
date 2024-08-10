import random, itertools, sys
from sdzkp.elementaryabeliansubgroup import ElementaryAbelianSubgroupWithSolution, ElementaryAbelianSubgroup
import hashlib
import base64

class SubgroupDistanceRound:
    def __init__(self) :
        # TODO: Check entropy of these random number generators, use CSPRNG
        self.s = random.randint(-1 * sys.maxsize, sys.maxsize)
        
        self.t_r = []
        self.r = []
        self.G = []
        self.t_u = []
        self.U = []
        self.R = []
        self.c = 0
        self.C1 = []
        self.C2 = []
        self.C3 = []
        self.round_result = False

    def set_seed(self, s):
        self.s = s
        random.seed(self.s)

    def hash(self, data):
        hashalg = hashlib.sha3_512()
        hashalg.update(repr(data).encode('utf-8'))
        digest = hashalg.digest()
        digest_base64 = base64.b64encode(digest)#.decode('utf-8')
        return digest_base64

    def generate_commitment(self, data):
        return self.hash(data)

    def generate_commitments(self):
        self.C1 = self.generate_commitment(self.Z1)
        self.C2 = self.generate_commitment(self.Z2)
        self.C3 = self.generate_commitment(self.s)

    def generate_random_array(self,n):
        print(f"Seed {self.s}")
        #systemrandom = SystemRandom()
        random.seed(self.s)
        self.R = [0]*n
        for i in range(n):
            self.R[i] = random.randint(-1 * sys.maxsize, sys.maxsize)
        
    
    def generate_Z1_and_Z2(self):
        self.Z1 = [a + b for a, b in zip(self.U, self.R)]
        self.Z2 = [a + b for a, b in zip(self.G, self.R)]

class SubgroupDistanceProblem:
    def __init__(self, generators, m, n, g, min_dist):
        self.m = m
        self.n = n
        self.generators_arrayform = generators  # The generators in array form
        self.K = min_dist # The minimum Hamming distance of H to pi
        self.g = g
        self.H = ElementaryAbelianSubgroup(self.n, self.generators_arrayform)
        self.round_data = {}

    @classmethod
    def create_from_linearized_generators(cls, linearized_generators, m, n, g, min_dist):
        generators = {}
        for i in range(round(m/2)):
            generators[(i,"t")]=linearized_generators[(2*i)*n:(2*i)*n+n]
            generators[(i,"f")]=linearized_generators[(2*i+1)*n:(2*i+1)*n+n]
        print("KKKKKKK = ", min_dist)
        return cls(generators, m, n, g, min_dist)

    def print_generators_arrayform(self):
        for i in range(self.p):
            print(f"π_t_{i}", self.generators_arrayform[(i,"t")][-12:])
            print(f"π_f_{i}", self.generators_arrayform[(i,"f")][-12:])

    def hamming_distance(self,p1, p2):
        """Calculate the Hamming distance between two permutations."""
        assert len(p1) == len(p2), "Permutations must be of the same length"
        return sum(1 for i in range(len(p1)) if p1[i] != p2[i])

    def linearize_generators(self):
        arr = []
        for i in range(self.p):
            arr.extend(self.generators_arrayform[(i,"t")])
            arr.extend(self.generators_arrayform[(i,"f")])
        return arr

class SubgroupDistanceProblemWithSolution(SubgroupDistanceProblem):
    def __init__(self, max2sat_instance):
        self.p = max2sat_instance.num_variables # Number of variables in max2sat (2*p is the number of generators of H)
        self.m = self.p *2 # The number of generators, "t" and "f" for each variable in max2sat
        self.q_original = max2sat_instance.num_clauses  # Number of clauses in max2sat instance, we will extend this
        self.clauses = list(max2sat_instance.clauses)  # Max2Sat clauses that will used in reduction to subgroup distance problem
        self.K_prime = max2sat_instance.k # maximum number of satisfied clauses in max2sat instance 
        self.q = 2 * self.K_prime + 3 # Number of so-called clauses in extended form for subgroup distance problem
        #self.n = self.p* (6*self.q + 2) + 6*self.q # The symmetric group Sn
        
        # The generator hashmap has the key (index,"t") or (index, "f") for keeping track of true (solution) and false (non-solution) transpositions
        self.generators = {} # The generators in binary representation for subgroup H in Sn (subgroup distance problem)
        self.generators_arrayform = {}  # The generators in array form
        self.generators_support = {} # Support is defined to be the number of 1s in the binary representation of a generator
        self.average_support = 0 # Average support of all generators

        # The SOLUTION to the subgroup distance problem
        # Multiplication of the solution generators will yield an element in H that has the minimum Hamming distance K to pi
        self.H = None # This will be elementary abelian subgroup H after reduction
        self.h = None # This is the solution for subgroup distance problem (multiplication of solution generators)
        self.max2sat_instance_solution = max2sat_instance.solution
        self.solution_t_h = self.convert_max2sat_solution_to_subgroupdistance_solution(max2sat_instance.solution)  # The solution to both max2sat (and indirectly to the extended subgroup distance problem)
        print("t_h =", self.solution_t_h)
        print("max2sat solution", max2sat_instance.solution)
        self.K = 6*self.q_original - 4*self.K_prime # The minimum Hamming distance of H to pi
        #print("FROMMAXSAT K=", self.K)
        self.reduce_to_sdp_and_extend() # Reduce max2sat to subgroup distance problem and extend
        self.num_transpositions_in_generators = len(self.generators[0,"t"])
        self.n = 2*self.num_transpositions_in_generators
        self.blinder = self.generate_random_blinder() # We will map these integers in pairs to transpositions
        
        self.convert_generators_to_arrayform_using_blinder()
        self.g = self.generate_permutation_g_in_Sn()
        #print("g", self.g[-(self.q-self.q_original)*6:])

        self.H_WithSolution = ElementaryAbelianSubgroupWithSolution(self.n, self.generators_arrayform, self.solution_t_h)
        self.h = self.H_WithSolution.h
        #print("h", self.h[-(self.q-self.q_original)*6:])
        check_K = self.hamming_distance(self.g, self.h)
        if check_K != self.K:
            print(f"There is some error in extension since {self.K}!={check_K}")
        super().__init__(self.generators_arrayform, self.m, self.n, self.g, self.K)
    
    def setup_sdzkp_round(self, round_id):
        rd = SubgroupDistanceRound()
                                             
        rd.t_r = self.H_WithSolution.random_binary_array()
        rd.r, rd.t_r = self.H_WithSolution.generate_element_from_bitarray(rd.t_r)
        print(len(self.g), len(rd.r))
        rd.t_u = [a ^ b for a, b in zip(self.H_WithSolution.solution_t_h, rd.t_r)]
        rd.U, rd.t_u = self.H_WithSolution.generate_element_from_bitarray(rd.t_u)
        rd.G = self.H_WithSolution.multiply_permutations(rd.r,self.g)
        rd.generate_random_array(self.n)
        distn = self.H_WithSolution.hamming_distance(self.g, self.h)
        print(f"Distance {distn}")
        rd.generate_Z1_and_Z2()
        rd.generate_commitments()

        print(round_id, self.H_WithSolution.solution_t_h, rd.t_r, rd.t_u)
        self.round_data[round_id] = rd
        return rd
        
    # def instance(self):
    #     # n, generators of H, pi, K
    #     flat_generator_array = [item for sublist in self.generators for item in sublist]
    #     return self.n, flat_generator_array, self.permutation_pi, self.K

    def convert_max2sat_solution_to_subgroupdistance_solution(self, solution):
        solution_t_h = [0]*2*self.p
        for i in range(len(solution)):
            if solution[i] == True:
                solution_t_h[2*i] = 1
            else:
                solution_t_h[2*i+1] = 1
        return solution_t_h

    def create_x_for_variable_i(self, i):
        num_transposition_in_x_i = 3*self.q+3 # Each transposition is represented as a bit 1: (a b) 0: (a)(b) in cycle notation
        # Add num_transposition_in_x_i number of 1's or 0's to generators
        zeros = [0 for _ in range( num_transposition_in_x_i)]
        ones  = [1 for _ in range( num_transposition_in_x_i)]
        x_i = []
        # If the generator k is mapped to variable i, then add 1s, otherwise add 0s
        for k in range(self.p):
            if k==i:
                x_i.extend(ones)
            else:
                x_i.extend(zeros)
        
        return x_i

    def create_y_for_variable_i_clause_j (self, i,j):
        leftconst  = [1,1,0]        # if the variable is in the left position of the clause
        rightconst = [1,0,1]        # if the variable is in the right position of the clause
        zerosconst = [0,0,0]        # default (no transposition)
        clause = self.clauses[j] 
        fret = zerosconst.copy()    # default return values for non-solution
        tret = zerosconst.copy()    # default return value for solution

        if clause[0][0] == i  and  not clause[0][1]:
            tret = leftconst.copy()     # if on the left and not negated
        elif clause[1][0] == i  and not clause[1][1]:
            tret = rightconst.copy()    # if on the right and not negated
        if clause[0][0] == i  and  clause[0][1]:
            fret = leftconst.copy()     # if on the left and negated
        elif clause[1][0] == i  and  clause[1][1]:
            fret = rightconst.copy()    # if on the right and negated

        return tret, fret  # the triplet for the true (solution) and false (non-solution) generators 

    def create_y_for_variable_i(self, i):
        ty_i = []
        fy_i = []
        # loop over each clause in max2sat and add a triplet as defined in create_y_for_variable_i_clause_j
        for k in range(self.q_original):
            ty_ij, fy_ij = self.create_y_for_variable_i_clause_j(i,k)
            ty_i.extend(ty_ij)
            fy_i.extend(fy_ij)
        return ty_i, fy_i

    def reduce_to_sdp_for_variable_i(self, i):
        tx_i = self.create_x_for_variable_i(i) # solution generator: x_i values guarantee that each generator mapped to a variable is chosen in solution
        fx_i = tx_i.copy()  # non-solution generator: x_i values guarantee that each generator mapped to a variable is chosen in solution
        ty_i, fy_i = self.create_y_for_variable_i(i) # the original clauses in max2sat are mapped to subgroup distance problem exactly
        
        tpi_i = tx_i.copy()     # Create true (solution) generator by first setting x_i bits
        fpi_i = fx_i.copy()     # Create false (non-solution) generator by first setting x_i bits
        tpi_i.extend(ty_i)      # Append y_i to true generator
        fpi_i.extend(fy_i)      # Append y_i to false generator
        
        return tpi_i, fpi_i
    
    def group_triplets(self, arr):
        # Group the array into triplets
        triplets = [arr[i:i+3] for i in range(len(arr)-3*self.q, len(arr), 3)]
        # Create a string representation of the triplets
        result = " ".join(["(" + " ".join(map(str, triplet)) + ")" for triplet in triplets])
        return result

    def print_generators(self):
        for i in range(self.p):
            if self.solution_t_h[2*i] == 1:
                print(f"π_t_{i}", self.group_triplets(self.generators[(i,"t")]), self.generators_support[(i,"t")], len(self.generators[(i,"t")]) - self.generators_support[(i,"t")])
            else:
                print(f"π_f_{i}", self.group_triplets(self.generators[(i,"f")]), self.generators_support[(i,"f")], len(self.generators[(i,"f")]) - self.generators_support[(i,"f")])

    def print_generators_arrayform(self):
        for i in range(self.p):
            #if self.solution_t_h[i] == False:
            print(f"π_t_{i}", self.generators_arrayform[(i,"t")][-34:], self.generators_support[(i,"t")], len(self.generators[(i,"t")]) - self.generators_support[(i,"t")])
            #else:
            print(f"π_f_{i}", self.generators_arrayform[(i,"f")][-34:], self.generators_support[(i,"f")], len(self.generators[(i,"f")]) - self.generators_support[(i,"f")])


    def generate_random_3bits(self, support):
        # If the support of the generator is less than the average support pick a random triplet to increase number of 1s
        # Otherwise pick a random triplet that has more 0s than 1s
        perms_of_large_number_of_0s = [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        perms_of_large_number_of_1s = [
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 1]
        ]
        if support<self.average_support:
            perms = perms_of_large_number_of_1s
        else:
            perms = perms_of_large_number_of_0s
        return random.choice(perms)
        


    def extend_generator(self, i, tf, random_bits):
        # extend the generator with triplet random_bits and update the support values
        self.generators[(i,tf)].extend(random_bits)
        self.generators_support[(i,tf)] = sum(self.generators[(i,tf)])
        
        # update the average support for all generators
        vals = self.generators_support.values()
        self.average_support = sum(vals)/len(vals)


    def add_random_3bits_to_solution_generators(self):
        sum_bits = [0, 0, 0]
        sum_bits_nonsolution = [0, 0, 0]
        random_bits_solution = []
        random_bits_nonsolution = []
        # Select a generator randomly, choose triplets for others randomly, 
        # Arrange the triplet for the selected generator accordingly
        # If solution then sum of triplets added to solution generators sum up to 1s to keep the Hamming distance the same
        # If non-solution then sum of triplets added to solution generators sum up to 0s to keep the Hamming distance the same or increase
        selectedsolution = random.randrange(self.p)
        # Add random 3-bit values to all arrays except the last one
        for i in range(self.p):
            if i == selectedsolution:
                continue # will add triplet out of loop for the selected generator
            if self.max2sat_instance_solution[i] == True:
                random_bits_solution = self.generate_random_3bits(self.generators_support[(i,"t")])
                self.extend_generator(i,"t", random_bits_solution)
                random_bits_nonsolution = self.generate_random_3bits(self.generators_support[(i,"f")])
                self.extend_generator(i,"f", random_bits_nonsolution)
            else:
                random_bits_solution = self.generate_random_3bits(self.generators_support[(i,"f")])
                self.extend_generator(i,"f", random_bits_solution)
                random_bits_nonsolution = self.generate_random_3bits(self.generators_support[(i,"t")])
                self.extend_generator(i,"t", random_bits_nonsolution)
            sum_bits = [(sum_bits[i] ^ random_bits_solution[i]) for i in range(3)]
            sum_bits_nonsolution = [(sum_bits_nonsolution[i] ^ random_bits_nonsolution[i]) for i in range(3)]

        # Determine the 3-bit value for the last array to ensure the sum is [1, 1, 1]
        required_bits_solution = [(1 - sum_bits[i]) for i in range(3)]
        required_bits_nonsolution = [(1- (1 ^ sum_bits_nonsolution[i])) for i in range(3)]
        #print(required_bits_nonsolution, sum_bits_nonsolution)
        if self.max2sat_instance_solution[selectedsolution] == 1: 
            self.extend_generator(selectedsolution,"t", required_bits_solution) # If variable is true in solution, the "t" generator is the solution
            self.extend_generator(selectedsolution,"f", required_bits_nonsolution)
        else:
            self.extend_generator(selectedsolution,"f", required_bits_solution) # If variable is false in solution, the "f" generator is the solution
            self.extend_generator(selectedsolution,"t", required_bits_nonsolution)
            


    def extend_sdp(self):
        # Move over all variables, add random triplets to solution variables (t or f) that sums up to (1,1,1)
        # Move over all variables, add random triplets to none solution variable (t or f) that increases number of zeros while
        # balancing the support (number of 1s) of each generator (balance: support must be almost equal for each generator!)
        self.add_random_3bits_to_solution_generators()
    
    def reduce_to_sdp_and_extend(self):
        for i in range(self.p):
            tpi_i, fpi_i = self.reduce_to_sdp_for_variable_i(i)
            self.generators[(i,"t")] = tpi_i
            self.generators[(i,"f")] = fpi_i
            self.generators_support[(i,"t")] = sum(tpi_i)
            self.generators_support[(i,"f")] = sum(fpi_i)
        for k in range(self.q-self.q_original):
            self.extend_sdp()
            #print("ADDING Random Extension Clause ", k)
        #self.print_generators()
    
    # TODO: remove not needed any more, brute force search
    def get_bit_i_of_generators(self, i):
        bit_array = [0]*2*self.p
        for j in range(self.p):
            bit_array[2*j] = self.generators[j,"t"][i]
            bit_array[2*j+1] = self.generators[j,"f"][i]
            
        return bit_array

    # TODO: remove not needed any more, brute force search
    def xor_and_check_combinations(self, bit_array, value, combinations=None):
        n = len(bit_array)
        all_combinations = []
        correct_combinations = []
        arr = list(range(n))

        if combinations == None:
            # Generate all combinations
            for r in range(1, n + 1):
                combinations = list(itertools.combinations(arr, r))
                all_combinations.extend(combinations)
        else:
            all_combinations = combinations # Prune the search space
       
        # Compute the XOR for each combination
        #xor_results = []
        for combination in all_combinations:
            xor_result = 0
            for num in combination:
                xor_result ^= bit_array[num]
            if value == xor_result:
                #print(combination, value, xor_result)
                correct_combinations.append(combination)
            #xor_results.append((combination, xor_result))
        
        return correct_combinations

    # TODO: remove not needed any more, brute force search
    def test_membership(self, perm):
        v = perm[0]
        bit_array = self.get_bit_i_of_generators(0)
        #print(bit_array)
        correct_combinations = self.xor_and_check_combinations(bit_array, v, combinations=None)
        for i in range(1, len(perm)):
            v = perm[i]
            bit_array = self.get_bit_i_of_generators(i)
            #print(bit_array)
            correct_combinations = self.xor_and_check_combinations(bit_array, v, combinations=correct_combinations)
            if len(correct_combinations)<=0:
                return False
        print(correct_combinations)
        if len(correct_combinations)>0:
            return True
        else:
            return False

    def convert_generators_to_arrayform_using_blinder(self):
        for i in range(self.p):
            generator_arrayform_t = self.convert_binary_permutation_to_arrayform_using_blinder(self.generators[(i,"t")])     
            generator_arrayform_f = self.convert_binary_permutation_to_arrayform_using_blinder(self.generators[(i,"f")])     
            self.generators_arrayform[(i,"t")] = generator_arrayform_t
            self.generators_arrayform[(i,"f")] = generator_arrayform_f
        #self.print_generators_arrayform()

    
    def convert_binary_permutation_to_arrayform_using_blinder(self, generator_v):
        generator_arrayform = [-1]*self.n
        for idx, t in enumerate (generator_v):
            #print(idx, t)
            if t==1:
                generator_arrayform[self.blinder[2*idx]] = self.blinder[2*idx+1]
                generator_arrayform[self.blinder[2*idx+1]] = self.blinder[2*idx]
            else:
                generator_arrayform[self.blinder[2*idx]] = self.blinder[2*idx]
                generator_arrayform[self.blinder[2*idx+1]] = self.blinder[2*idx+1]          
        return generator_arrayform
    
    def generate_permutation_g_in_Sn(self):
        ones = [1]*round(self.n/2)
        g = self.convert_binary_permutation_to_arrayform_using_blinder(ones)
        return g

    def generate_random_blinder(self):       
        # Generate the list of integers from 0 to n-1
        blinder = list(range(self.n ))
        #print("blinder", blinder)
        # Shuffle the list of integers to randomize their order
        #random.shuffle(blinder)
        return blinder

