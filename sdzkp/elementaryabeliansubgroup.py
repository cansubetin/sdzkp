import random, math
from functools import reduce
from collections import deque


class ElementaryAbelianSubgroup:
    def __init__(self, n, generators):
        self.generators = generators # Store all generators generators
        self.n = n # PermutationGroup H with these "generators" is a subgroup of Symmetric Group, Sn
        self.identity = list(range(self.n)) #Identity
        self.m = len(self.generators) # The number of generators in Permutation Group H

    def is_valid_permutation(self, perm):
        return sorted(perm) == list(range(self.n)) 

    def transpose(self, perm, i, j):
        if not (0 <= i < len(perm) and 0 <= j < len(perm)):
            raise IndexError("Indices out of range")
        perm[i], perm[j] = perm[j], perm[i]
        return perm

    def multiply_permutations(self, perm1, perm2):
        return [perm1[perm2[i]] for i in range(self.n)]

    
    def multiply_generators(self):
        def apply_permutation(perm, array):
            return [array[i] for i in perm]
        # Apply permutations in sequence
        result = reduce(apply_permutation, reversed(self.generators), self.identity)
        
        return result

    def inverse(self, perm):
        inverse_perm = [0] * self.n
        for i in range(self.n):
            inverse_perm[perm[i]] = i
        return ElementaryAbelianSubgroup([inverse_perm])


    def random_binary_array(self):
        # Generate random array of 0s and 1s
        array = [random.randint(0, 1) for _ in range(self.m)]
        # Ensure at least one 1
        #if 1 not in array:
        #    array[random.randint(0, self.m-1)] = 1
        return array



    def generate_element_from_bitarray(self, bit_array):
        combined_permutation = self.identity[:]
        temp = math.ceil(len(bit_array)/2)
        for i in range(temp):
            if bit_array[2*i] == 1:
                #print("using ", 2*i)
                combined_permutation = self.multiply_permutations(combined_permutation, self.generators[(i,"t")])
            if bit_array[2*i+1] == 1:
                #print("using ", 2*i+1)
                combined_permutation = self.multiply_permutations(combined_permutation, self.generators[(i,"f")])
        return combined_permutation, bit_array


    def random_element(self):
        t_r = self.random_binary_array()
        combined_permutation,_ = self.generate_element_from_bitarray(t_r)
        return combined_permutation, t_r

    def solve(self, g):
        all_elements = self.generate_all_elements()
        mindist = self.n+1
        chosenelem = None
        for elem in all_elements:
            dist = self.hamming_distance(g, elem)
            if dist<mindist:
                chosenelem = elem
                mindist = dist
        return chosenelem, mindist

    def hamming_distance(self,p1, p2):
        """Calculate the Hamming distance between two permutations."""
        assert len(p1) == len(p2), "Permutations must be of the same length"
        return sum(1 for i in range(len(p1)) if p1[i] != p2[i])

    def generate_all_elements(self):
        visited = set()
        queue = deque([self.identity])
        all_elements = []
        
        while queue:
            current = queue.popleft()
            perm_tuple = tuple(current)
            if perm_tuple not in visited:
                visited.add(perm_tuple)
                all_elements.append(current)
                for gen in self.generators.values():
                    next_perm = self.multiply_permutations(current, gen)
                    queue.append(next_perm)
        
        return all_elements

    def print_all_elements(self):
        print("All elements in the permutation group:")
        all_elements = self.generate_all_elements()
        
        for elem in all_elements:
            print("elem: ", elem[-12:])

    def inverse_permutation(self, perm):
        return perm # Since we use only transpositions, the order of elements are two, hence they are inverses of themselves

    def apply_generators(self, bitmask):
        # The bitmask is of length m, if 1 in bitmask_i, multiply the ith generator
        current_perm = self.identity[:]
        for i in range(len(self.generators)):
            if bitmask & (1 << i):
                current_perm = self.multiply_permutations(current_perm, self.generators[i])
        return current_perm

    def __repr__(self):
        return f"PermutationGroup(n={self.n}, permutation={self.generators})"

    def __eq__(self, other):
        return self.permutation == other.permutation


class ElementaryAbelianSubgroupWithSolution(ElementaryAbelianSubgroup):
    def __init__(self, n, generators, solution_t_h):
        super().__init__(n, generators)
        self.solution_t_h = solution_t_h # Store generators that produce the solution
        self.h, bit_array = self.multiply_solution_generators() # This is the solution (h in PermutationGroup H) of the subgroup distance problem
        #print("CHECKKKKKKKK  ", self.solution_t_h, self.h)

    def multiply_solution_generators(self):
        # combined_permutation = self.identity[:]
        # for i in range(round(self.m/2)):
        #     if self.solution_t_h[i] == 1:
        #         combined_permutation = self.multiply_permutations(combined_permutation, self.generators[(i,"t")])
        #     else:
        #         combined_permutation = self.multiply_permutations(combined_permutation, self.generators[(i,"f")])
        combined_permutation, bit_array = self.generate_element_from_bitarray(self.solution_t_h)
        return combined_permutation, bit_array
    