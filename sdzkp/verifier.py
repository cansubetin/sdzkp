from sdzkp.sdzkproto import sdzkp_pb2
from sdzkp.sgd import SubgroupDistanceProblem, SubgroupDistanceRound
import random

class Verifier:
    """
    The Verifier class is responsible for verifying the proofs provided by the Prover in the Zero-Knowledge Proof (ZKP)
    protocol for the Subgroup Distance Problem (SGD).

    Attributes:
        instance_id (str): A unique identifier for the problem instance.
        SGD (SubgroupDistanceProblem): The instance of the Subgroup Distance Problem.
    """

    def __init__(self, instance_id) -> None:
        """
        Initializes the Verifier with a given instance ID.

        Parameters:
            instance_id (str): A unique identifier for the problem instance.
        """
        self.instance_id = instance_id

    def handleSetup(self, sgdinst: sdzkp_pb2.SGDInstance):
        """
        Handles the setup phase by creating a Subgroup Distance Problem instance from the provided data.

        Parameters:
            sgdinst (sdzkp_pb2.SGDInstance): The SGD instance received from the Prover.

        Returns:
            sdzkp_pb2.SetupAck: An acknowledgment message indicating whether the setup was successful.
        """
        self.SGD = SubgroupDistanceProblem.create_from_linearized_generators(
            sgdinst.generators, sgdinst.m, sgdinst.n, sgdinst.g, sgdinst.min_distance
        )
        # TODO: Check corner cases and return false if the problem is not accepted
        return sdzkp_pb2.SetupAck(sgdid=sgdinst.sgdid, setupresult=True)

    def handleCommit(self, commitments):
        """
        Handles the commit phase by storing the commitments and generating a challenge.

        Parameters:
            commitments (sdzkp_pb2.Commitments): The commitments received from the Prover.

        Returns:
            sdzkp_pb2.Challenge: A challenge message to be sent to the Prover.
        """
        # TODO: Check whether this round is repeated or not!
        rd = SubgroupDistanceRound()
        rd.C1 = commitments.C1
        rd.C2 = commitments.C2
        rd.C3 = commitments.C3
        self.SGD.round_data[commitments.roundid] = rd
        c = random.randint(0, 2)
        rd.c = c
        return sdzkp_pb2.Challenge(sgdid=commitments.sgdid, roundid=commitments.roundid, challenge=c)

    def verify_0(self, rd: SubgroupDistanceRound, Z1, s, t_u):
        """
        Verifies the proof for the challenge c=0.

        Parameters:
            rd (SubgroupDistanceRound): The round data.
            Z1 (list): The Z1 value received from the Prover.
            s (int): The seed used for random generation.
            t_u (list): The t_u value received from the Prover.

        Returns:
            bool: True if the verification succeeds, False otherwise.
        """
        retval = True
        rd.set_seed(s)
        rd.Z1 = Z1
        rd.generate_random_array(self.SGD.n)

        rd.U, rd.t_u = self.SGD.H.generate_element_from_bitarray(t_u)
        Z1_minus_R = [a - b for a, b in zip(Z1, rd.R)]
        if Z1_minus_R != rd.U:
            retval = False
        else:
            expected_C1 = rd.generate_commitment(Z1)
            if rd.C1 != expected_C1:
                retval = False
            else:
                expected_C3 = rd.generate_commitment(s)
                if expected_C3 != rd.C3:
                    retval = False

        return retval

    def verify_1(self, rd: SubgroupDistanceRound, Z2, s, t_r):
        """
        Verifies the proof for the challenge c=1.

        Parameters:
            rd (SubgroupDistanceRound): The round data.
            Z2 (list): The Z2 value received from the Prover.
            s (int): The seed used for random generation.
            t_r (list): The t_r value received from the Prover.

        Returns:
            bool: True if the verification succeeds, False otherwise.
        """
        retval = True
        rd.set_seed(s)
        rd.Z2 = Z2
        rd.generate_random_array(self.SGD.n)

        rd.r, rd.t_r = self.SGD.H.generate_element_from_bitarray(t_r)
        rd.G = self.SGD.H.multiply_permutations(rd.r, self.SGD.g)

        Z2_minus_R = [a - b for a, b in zip(Z2, rd.R)]
        if Z2_minus_R != rd.G:
            retval = False
        else:
            expected_C2 = rd.generate_commitment(Z2)
            if rd.C2 != expected_C2:
                retval = False
            else:
                expected_C3 = rd.generate_commitment(s)
                if expected_C3 != rd.C3:
                    retval = False

        return retval

    def verify_2(self, rd: SubgroupDistanceRound, Z1, Z2):
        """
        Verifies the proof for the challenge c=2.

        Parameters:
            rd (SubgroupDistanceRound): The round data.
            Z1 (list): The Z1 value received from the Prover.
            Z2 (list): The Z2 value received from the Prover.

        Returns:
            bool: True if the verification succeeds, False otherwise.
        """
        retval = True
        Z1_minus_Z2 = [a - b for a, b in zip(Z1, Z2)]
        nonzero_count = sum(1 for x in Z1_minus_Z2 if x != 0)
        if nonzero_count > self.SGD.K:
            retval = False
        else:
            expected_C1 = rd.generate_commitment(Z1)
            if rd.C1 != expected_C1:
                retval = False
            else:
                expected_C2 = rd.generate_commitment(Z2)
                if rd.C2 != expected_C2:
                    retval = False

        return retval

    def handleVerify(self, response):
        """
        Handles the verification phase by verifying the Prover's response to the challenge.

        Parameters:
            response (sdzkp_pb2.Response): The response received from the Prover.

        Returns:
            sdzkp_pb2.VerificationResult: The result of the verification.
        """
        rd = self.SGD.round_data[response.roundid]
        res = False
        match rd.c:
            case 0:
                res = self.verify_0(rd, response.Z1, response.s, response.t_u)
            case 1:
                res = self.verify_1(rd, response.Z2, response.s, response.t_r)
            case 2:
                res = self.verify_2(rd, response.Z1, response.Z2)
            case _:
                print("Error in challenge, abort")

        return sdzkp_pb2.VerificationResult(sgdid=response.sgdid, roundid=response.roundid, roundresult=res, verificationresult=res)
