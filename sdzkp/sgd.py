import random, itertools, sys
from sdzkp.elementaryabeliansubgroup import ElementaryAbelianSubgroupWithSolution, ElementaryAbelianSubgroup
import hashlib
import base64

class SubgroupDistanceRound:
    """
    A class representing a single round in the SDZKP.

    Attributes:
        s (int): A random seed for generating randomness.
        t_r (list): A bit array for random elements.
        r (list): A randomly generated element.
        G (list): A permuted element.
        t_u (list): A bit array for another random element.
        U (list): A second permuted element.
        R (list): A random array of integers.
        c (int): A challenge bit.
        C1, C2, C3 (list): Commitments generated during the round.
        round_result (bool): The result of the round.
    """
    
    def __init__(self):
        """
        Initializes a SubgroupDistanceRound instance.
        """
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
        """
        Sets the random seed.

        Parameters:
            s (int): The seed to set.
        """
        self.s = s
        random.seed(self.s)

    def hash(self, data):
        """
        Computes the SHA3-512 hash of the given data and encodes it in base64.

        Parameters:
            data: The data to hash.

        Returns:
            bytes: The base64-encoded hash.
        """
        hashalg = hashlib.sha3_512()
        hashalg.update(repr(data).encode('utf-8'))
        digest = hashalg.digest()
        digest_base64 = base64.b64encode(digest)
        return digest_base64

    def generate_commitment(self, data):
        """
        Generates a cryptographic commitment for the given data.

        Parameters:
            data: The data to commit to.

        Returns:
            bytes: The commitment (hash).
        """
        return self.hash(data)

    def generate_commitments(self):
        """
        Generates the commitments C1, C2, and C3 based on Z1, Z2, and the seed.
        """
        self.C1 = self.generate_commitment(self.Z1)
        self.C2 = self.generate_commitment(self.Z2)
        self.C3 = self.generate_commitment(self.s)

    def generate_random_array(self, n):
        """
        Generates a random array of integers.

        Parameters:
            n (int): The length of the array.
        """
        random.seed(self.s)
        self.R = [random.randint(-1 * sys.maxsize, sys.maxsize) for _ in range(n)]
        
    def generate_Z1_and_Z2(self):
        """
        Generates Z1 and Z2 as the sum of U and R, and G and R, respectively.
        """
        self.Z1 = [a + b for a, b in zip(self.U, self.R)]
        self.Z2 = [a + b for a, b in zip(self.G, self.R)]


class SubgroupDistanceProblem:
    """
    A class representing the subgroup distance problem.

    Attributes:
        m (int): The number of generators.
        n (int): The size of the symmetric group.
        generators_arrayform (dict): The generators in array form.
        K (int): The minimum Hamming distance.
        g (list): A target permutation.
        H (ElementaryAbelianSubgroup): The elementary abelian subgroup.
        round_data (dict): Data for each round.
    """
    
    def __init__(self, generators, m, n, g, min_dist):
        """
        Initializes a SubgroupDistanceProblem instance.

        Parameters:
            generators (dict): The generators in array form.
            m (int): The number of generators.
            n (int): The size of the symmetric group.
            g (list): The target permutation.
            min_dist (int): The minimum Hamming distance.
        """
        self.m = m
        self.n = n
        self.generators_arrayform = generators
        self.K = min_dist
        self.g = g
        self.H = ElementaryAbelianSubgroup(self.n, self.generators_arrayform)
        self.round_data = {}

    @classmethod
    def create_from_linearized_generators(cls, linearized_generators, m, n, g, min_dist):
        """
        Creates an instance of SubgroupDistanceProblem from linearized generators.

        Parameters:
            linearized_generators (list): A list of linearized generators.
            m (int): The number of generators.
            n (int): The size of the symmetric group.
            g (list): The target permutation.
            min_dist (int): The minimum Hamming distance.

        Returns:
            SubgroupDistanceProblem: An initialized instance.
        """
        generators = {}
        for i in range(round(m/2)):
            generators[(i,"t")] = linearized_generators[(2*i)*n:(2*i)*n+n]
            generators[(i,"f")] = linearized_generators[(2*i+1)*n:(2*i+1)*n+n]
        return cls(generators, m, n, g, min_dist)

    def print_generators_arrayform(self):
        """
        Prints the generators in array form.
        """
        for i in range(self.p):
            print(f"π_t_{i}", self.generators_arrayform[(i,"t")][-12:])
            print(f"π_f_{i}", self.generators_arrayform[(i,"f")][-12:])

    def hamming_distance(self, p1, p2):
        """
        Calculates the Hamming distance between two permutations.

        Parameters:
            p1 (list): The first permutation.
            p2 (list): The second permutation.

        Returns:
            int: The Hamming distance.
        """
        assert len(p1) == len(p2), "Permutations must be of the same length"
        return sum(1 for i in range(len(p1)) if p1[i] != p2[i])

    def linearize_generators(self):
        """
        Linearizes the generators for storage or processing.

        Returns:
            list: A list of linearized generators.
        """
        arr = []
        for i in range(self.p):
            arr.extend(self.generators_arrayform[(i,"t")])
            arr.extend(self.generators_arrayform[(i,"f")])
        return arr


class SubgroupDistanceProblemWithSolution(SubgroupDistanceProblem):
    """
    A subclass of SubgroupDistanceProblem that includes a solution.

    Attributes:
        p (int): The number of variables in the max2sat instance.
        m (int): The number of generators.
        q_original (int): The number of clauses in the max2sat instance.
        clauses (list): The max2sat clauses.
        K_prime (int): The maximum number of satisfied clauses in the max2sat instance.
        q (int): The number of extended clauses for the subgroup distance problem.
        generators (dict): The generators in binary form.
        generators_arrayform (dict): The generators in array form.
        generators_support (dict): The support of each generator.
        average_support (int): The average support of all generators.
        H (ElementaryAbelianSubgroup): The elementary abelian subgroup.
        h (list): The solution for the subgroup distance problem.
        max2sat_instance_solution (list): The solution to the max2sat instance.
        solution_t_h (list): The solution in bit array form.
        K (int): The minimum Hamming distance.
        num_transpositions_in_generators (int): The number of transpositions in the generators.
        n (int): The size of the symmetric group.
        blinder (list): A list used to map integers to transpositions.
        g (list): The permutation g in Sn.
        H_WithSolution (ElementaryAbelianSubgroupWithSolution): The elementary abelian subgroup with the solution.
    """
    
    def __init__(self, max2sat_instance):
        """
        Initializes a SubgroupDistanceProblemWithSolution instance.

        Parameters:
            max2sat_instance: An instance of the max2sat problem.
        """
        #self.max2sat_instance = max2sat_instance
        self.p = max2sat_instance.num_variables
        self.m = self.p * 2
        self.q_original = max2sat_instance.num_clauses
        self.clauses = list(max2sat_instance.clauses)
        self.K_prime = max2sat_instance.k
        self.q = 2 * self.K_prime + 3
        
        self.generators = {}
        self.generators_arrayform = {}
        self.generators_support = {}
        self.average_support = 0
        
        self.H = None
        self.h = None
        self.max2sat_instance_solution = max2sat_instance.solution
        self.solution_t_h = self.convert_max2sat_solution_to_subgroupdistance_solution(max2sat_instance.solution)
        self.K = 6*self.q_original - 4*self.K_prime
        self.reduce_to_sdp_and_extend()
        self.num_transpositions_in_generators = len(self.generators[0, "t"])
        self.n = 2 * self.num_transpositions_in_generators
        self.blinder = self.generate_random_blinder()
        
        self.convert_generators_to_arrayform_using_blinder()
        self.g = self.generate_permutation_g_in_Sn()
        
        self.H_WithSolution = ElementaryAbelianSubgroupWithSolution(self.n, self.generators_arrayform, self.solution_t_h)
        self.h = self.H_WithSolution.h
        check_K = self.hamming_distance(self.g, self.h)
        if check_K != self.K:
            print(f"There is some error in extension since {self.K}!={check_K}")
        super().__init__(self.generators_arrayform, self.m, self.n, self.g, self.K)
    
    def setup_sdzkp_round(self, round_id):
        """
        Sets up a round of the Subgroup Distance Zero-Knowledge Proof (SDZKP).

        Parameters:
            round_id (int): The ID of the round.

        Returns:
            SubgroupDistanceRound: The initialized round.
        """
        rd = SubgroupDistanceRound()                                             
        rd.t_r = self.H_WithSolution.random_binary_array()
        rd.r, _ = self.H_WithSolution.generate_element_from_bitarray(rd.t_r)
        rd.t_u = [a ^ b for a, b in zip(self.solution_t_h, rd.t_r)]
        rd.U, rd.t_u = self.H_WithSolution.generate_element_from_bitarray(rd.t_u)
        rd.G = self.H_WithSolution.multiply_permutations(rd.r, self.g)
        rd.generate_random_array(self.n)
        distn = self.H_WithSolution.hamming_distance(self.g, self.h)
        rd.generate_Z1_and_Z2()
        rd.generate_commitments()

        self.round_data[round_id] = rd
        return rd

    def convert_max2sat_solution_to_subgroupdistance_solution(self, solution):
        """
        Converts a max2sat solution to a solution for the subgroup distance problem.

        Parameters:
            solution (list): The max2sat solution.

        Returns:
            list: The corresponding solution for the subgroup distance problem.
        """
        solution_t_h = [0] * 2 * self.p
        for i in range(len(solution)):
            if solution[i]:
                solution_t_h[2 * i] = 1
            else:
                solution_t_h[2 * i + 1] = 1
        return solution_t_h

    def create_x_for_variable_i(self, i):
        """
        Creates the x_i vector for a variable in the subgroup distance problem.

        Parameters:
            i (int): The index of the variable.

        Returns:
            list: The x_i vector.
        """
        num_transposition_in_x_i = 3*self.q+3
        zeros = [0 for _ in range(num_transposition_in_x_i)]
        ones  = [1 for _ in range(num_transposition_in_x_i)]
        x_i = []
        for k in range(self.p):
            if k == i:
                x_i.extend(ones)
            else:
                x_i.extend(zeros)
        return x_i

    def create_y_for_variable_i_clause_j(self, i, j):
        """
        Creates the y_ij vector for a variable and a clause in the subgroup distance problem.

        Parameters:
            i (int): The index of the variable.
            j (int): The index of the clause.

        Returns:
            tuple: A tuple containing the y_ij vector for the true and false cases.
        """
        leftconst  = [1, 1, 0]
        rightconst = [1, 0, 1]
        zerosconst = [0, 0, 0]
        clause = self.clauses[j]
        fret = zerosconst.copy()
        tret = zerosconst.copy()

        if clause[0][0] == i and not clause[0][1]:
            tret = leftconst.copy()
        elif clause[1][0] == i and not clause[1][1]:
            tret = rightconst.copy()
        if clause[0][0] == i and clause[0][1]:
            fret = leftconst.copy()
        elif clause[1][0] == i and clause[1][1]:
            fret = rightconst.copy()

        return tret, fret

    def create_y_for_variable_i(self, i):
        """
        Creates the y_i vector for a variable in the subgroup distance problem.

        Parameters:
            i (int): The index of the variable.

        Returns:
            tuple: A tuple containing the y_i vector for the true and false cases.
        """
        ty_i = []
        fy_i = []
        for k in range(self.q_original):
            ty_ij, fy_ij = self.create_y_for_variable_i_clause_j(i, k)
            ty_i.extend(ty_ij)
            fy_i.extend(fy_ij)
        return ty_i, fy_i

    def reduce_to_sdp_for_variable_i(self, i):
        """
        Reduces the subgroup distance problem for a variable.

        Parameters:
            i (int): The index of the variable.

        Returns:
            tuple: A tuple containing the true and false generators.
        """
        tx_i = self.create_x_for_variable_i(i)
        fx_i = tx_i.copy()
        ty_i, fy_i = self.create_y_for_variable_i(i)
        
        tpi_i = tx_i.copy()
        fpi_i = fx_i.copy()
        tpi_i.extend(ty_i)
        fpi_i.extend(fy_i)
        
        return tpi_i, fpi_i
    
    def group_triplets(self, arr):
        """
        Groups an array into triplets and returns them as a string.

        Parameters:
            arr (list): The array to group.

        Returns:
            str: A string representation of the triplets.
        """
        triplets = [arr[i:i+3] for i in range(len(arr)-3*self.q, len(arr), 3)]
        result = " ".join(["(" + " ".join(map(str, triplet)) + ")" for triplet in triplets])
        return result

    def print_generators(self):
        """
        Prints the generators of the subgroup distance problem.
        """
        for i in range(self.p):
            if self.solution_t_h[2 * i] == 1:
                print(f"π_t_{i}", self.group_triplets(self.generators[(i, "t")]), self.generators_support[(i, "t")], len(self.generators[(i, "t")]) - self.generators_support[(i, "t")])
            else:
                print(f"π_f_{i}", self.group_triplets(self.generators[(i, "f")]), self.generators_support[(i, "f")], len(self.generators[(i, "f")]) - self.generators_support[(i, "f")])

    def print_generators_arrayform(self):
        """
        Prints the generators in array form for the subgroup distance problem.
        """
        for i in range(self.p):
            print(f"π_t_{i}", self.generators_arrayform[(i,"t")][-34:], self.generators_support[(i,"t")], len(self.generators[(i,"t")]) - self.generators_support[(i,"t")])
            print(f"π_f_{i}", self.generators_arrayform[(i,"f")][-34:], self.generators_support[(i,"f")], len(self.generators[(i,"f")]) - self.generators_support[(i,"f")])

    def generate_random_3bits(self, support):
        """
        Generates a random 3-bit vector based on the support of a generator.

        Parameters:
            support (int): The support of the generator.

        Returns:
            list: A 3-bit vector.
        """
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
        if support < self.average_support:
            perms = perms_of_large_number_of_1s
        else:
            perms = perms_of_large_number_of_0s
        return random.choice(perms)

    def extend_generator(self, i, tf, random_bits):
        """
        Extends a generator with random bits and updates its support.

        Parameters:
            i (int): The index of the generator.
            tf (str): Indicates whether the generator is "t" or "f".
            random_bits (list): The random bits to add.
        """
        self.generators[(i, tf)].extend(random_bits)
        self.generators_support[(i, tf)] = sum(self.generators[(i, tf)])
        
        vals = self.generators_support.values()
        self.average_support = sum(vals) / len(vals)

    def add_random_3bits_to_solution_generators(self):
        """
        Adds random 3-bit vectors to the solution generators to balance the Hamming distance.
        """
        sum_bits = [0, 0, 0]
        sum_bits_nonsolution = [0, 0, 0]
        random_bits_solution = []
        random_bits_nonsolution = []
        selectedsolution = random.randrange(self.p)
        for i in range(self.p):
            if i == selectedsolution:
                continue
            if self.max2sat_instance_solution[i]:
                random_bits_solution = self.generate_random_3bits(self.generators_support[(i, "t")])
                self.extend_generator(i, "t", random_bits_solution)
                random_bits_nonsolution = self.generate_random_3bits(self.generators_support[(i, "f")])
                self.extend_generator(i, "f", random_bits_nonsolution)
            else:
                random_bits_solution = self.generate_random_3bits(self.generators_support[(i, "f")])
                self.extend_generator(i, "f", random_bits_solution)
                random_bits_nonsolution = self.generate_random_3bits(self.generators_support[(i, "t")])
                self.extend_generator(i, "t", random_bits_nonsolution)
            sum_bits = [(sum_bits[i] ^ random_bits_solution[i]) for i in range(3)]
            sum_bits_nonsolution = [(sum_bits_nonsolution[i] ^ random_bits_nonsolution[i]) for i in range(3)]

        required_bits_solution = [(1 - sum_bits[i]) for i in range(3)]
        required_bits_nonsolution = [(1 - (1 ^ sum_bits_nonsolution[i])) for i in range(3)]
        if self.max2sat_instance_solution[selectedsolution]:
            self.extend_generator(selectedsolution, "t", required_bits_solution)
            self.extend_generator(selectedsolution, "f", required_bits_nonsolution)
        else:
            self.extend_generator(selectedsolution, "f", required_bits_solution)
            self.extend_generator(selectedsolution, "t", required_bits_nonsolution)

    def extend_sdp(self):
        """
        Extends the subgroup distance problem by adding random triplets to the solution generators.
        """
        self.add_random_3bits_to_solution_generators()
    
    def reduce_to_sdp_and_extend(self):
        """
        Reduces the max2sat problem to the subgroup distance problem and extends it.
        """
        for i in range(self.p):
            tpi_i, fpi_i = self.reduce_to_sdp_for_variable_i(i)
            self.generators[(i, "t")] = tpi_i
            self.generators[(i, "f")] = fpi_i
            self.generators_support[(i, "t")] = sum(tpi_i)
            self.generators_support[(i, "f")] = sum(fpi_i)
        for k in range(self.q - self.q_original):
            self.extend_sdp()
    
    def get_bit_i_of_generators(self, i):
        """
        Retrieves the i-th bit of all generators.

        Parameters:
            i (int): The bit index.

        Returns:
            list: A list of the i-th bits of all generators.
        """
        bit_array = [0] * 2 * self.p
        for j in range(self.p):
            bit_array[2 * j] = self.generators[j, "t"][i]
            bit_array[2 * j + 1] = self.generators[j, "f"][i]
        return bit_array

    def xor_and_check_combinations(self, bit_array, value, combinations=None):
        """
        Performs XOR on all combinations of the bit array and checks for a match with the value.

        Parameters:
            bit_array (list): The array of bits.
            value (int): The value to match.
            combinations (list, optional): A list of combinations to check. Defaults to None.

        Returns:
            list: A list of correct combinations.
        """
        n = len(bit_array)
        all_combinations = []
        correct_combinations = []
        arr = list(range(n))

        if combinations is None:
            for r in range(1, n + 1):
                combinations = list(itertools.combinations(arr, r))
                all_combinations.extend(combinations)
        else:
            all_combinations = combinations

        for combination in all_combinations:
            xor_result = 0
            for num in combination:
                xor_result ^= bit_array[num]
            if value == xor_result:
                correct_combinations.append(combination)
        
        return correct_combinations

    def test_membership(self, perm):
        """
        Tests if a permutation is a member of the group.

        Parameters:
            perm (list): The permutation to test.

        Returns:
            bool: True if the permutation is a member, False otherwise.
        """
        v = perm[0]
        bit_array = self.get_bit_i_of_generators(0)
        correct_combinations = self.xor_and_check_combinations(bit_array, v)
        for i in range(1, len(perm)):
            v = perm[i]
            bit_array = self.get_bit_i_of_generators(i)
            correct_combinations = self.xor_and_check_combinations(bit_array, v, combinations=correct_combinations)
            if not correct_combinations:
                return False
        return bool(correct_combinations)

    def convert_generators_to_arrayform_using_blinder(self):
        """
        Converts the binary representation of the generators to array form using a blinder.
        """
        for i in range(self.p):
            generator_arrayform_t = self.convert_binary_permutation_to_arrayform_using_blinder(self.generators[(i, "t")])     
            generator_arrayform_f = self.convert_binary_permutation_to_arrayform_using_blinder(self.generators[(i, "f")])     
            self.generators_arrayform[(i, "t")] = generator_arrayform_t
            self.generators_arrayform[(i, "f")] = generator_arrayform_f

    def convert_binary_permutation_to_arrayform_using_blinder(self, generator_v):
        """
        Converts a binary permutation to array form using a blinder.

        Parameters:
            generator_v (list): The binary permutation.

        Returns:
            list: The permutation in array form.
        """
        generator_arrayform = [-1] * self.n
        for idx, t in enumerate(generator_v):
            if t == 1:
                generator_arrayform[self.blinder[2 * idx]] = self.blinder[2 * idx + 1]
                generator_arrayform[self.blinder[2 * idx + 1]] = self.blinder[2 * idx]
            else:
                generator_arrayform[self.blinder[2 * idx]] = self.blinder[2 * idx]
                generator_arrayform[self.blinder[2 * idx + 1]] = self.blinder[2 * idx + 1]
        return generator_arrayform
    
    def generate_permutation_g_in_Sn(self):
        """
        Generates a permutation g in Sn.

        Returns:
            list: The generated permutation.
        """
        ones = [1] * round(self.n / 2)
        g = self.convert_binary_permutation_to_arrayform_using_blinder(ones)
        return g

    def generate_random_blinder(self):       
        """
        Generates a random blinder for mapping integers to transpositions.

        Returns:
            list: The blinder.
        """
        blinder = list(range(self.n))
        # Shuffle the list of integers to randomize their order
        random.shuffle(blinder)
        return blinder
