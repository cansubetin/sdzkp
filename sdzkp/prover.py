from sdzkp.max2sat import Max2SAT
from sdzkp.sgd import SubgroupDistanceProblemWithSolution, SubgroupDistanceRound
from sdzkp.sdzkproto import sdzkp_pb2


class Prover:
    """
    The Prover class is responsible for setting up and executing rounds of a Zero-Knowledge Proof (ZKP) protocol 
    for the Subgroup Distance Problem (SGD) derived from a Max2SAT instance.

    Attributes:
        grpc_stub: The gRPC stub for communication.
        instance_id (str): A unique identifier for the problem instance.
        number_of_rounds (int): The number of ZKP rounds to execute.
        SGD (SubgroupDistanceProblemWithSolution): An instance of the Subgroup Distance Problem with a solution.
    """

    def __init__(self, grpc_stub, instance_id, number_of_rounds, num_variables):
        """
        Initializes the Prover with a Max2SAT instance and converts it to a Subgroup Distance Problem.

        Parameters:
            grpc_stub: The gRPC stub for communication.
            instance_id (str): A unique identifier for the problem instance.
            number_of_rounds (int): The number of ZKP rounds to execute.
            num_variables (int): The number of variables in the Max2SAT instance.
        """
        self.grpc_stub = grpc_stub
        self.instance_id = str(instance_id)
        self.number_of_rounds = number_of_rounds
        max2satinstance = Max2SAT(num_variables=num_variables)
        max2satinstance.generate_instance_motoki()
        self.SGD = SubgroupDistanceProblemWithSolution(max2satinstance)

    def setup(self):
        """
        Sets up the Subgroup Distance Problem instance and sends it to the verifier via gRPC.

        Returns:
            bool: True if the setup was successful, False otherwise.
        """
        linearized_generators = self.SGD.linearize_generators()
        sgdinstance = sdzkp_pb2.SGDInstance(
            sgdid=self.instance_id,
            g=self.SGD.g,
            n=self.SGD.n,
            m=self.SGD.H.m,
            generators=linearized_generators,
            min_distance=self.SGD.K,
            number_of_rounds=self.number_of_rounds
        )
        setupackmessage = self.grpc_stub.Setup(sgdinstance)
        return setupackmessage.setupresult

    def commit(self, round_id):
        """
        Generates commitments for a given round and sends them to the verifier.

        Parameters:
            round_id (int): The ID of the current round.

        Returns:
            int: The challenge received from the verifier.
        """
        rd = self.SGD.setup_sdzkp_round(round_id)
        commitmsg = sdzkp_pb2.Commitments(
            sgdid=self.instance_id,
            roundid=round_id,
            C1=rd.C1,
            C2=rd.C2,
            C3=rd.C3
        )
        challengemessage = self.grpc_stub.Commit(commitmsg)
        return challengemessage.challenge

    def response(self, round_id, c):
        """
        Responds to the challenge from the verifier based on the commitments made.

        Parameters:
            round_id (int): The ID of the current round.
            c (int): The challenge received from the verifier.

        Returns:
            tuple: The result of the current round and the overall verification result.
        """
        rd = self.SGD.round_data[round_id]
        responsemessage = None
        match c:
            case 0:
                responsemessage = sdzkp_pb2.Response(
                    sgdid=self.instance_id,
                    roundid=round_id,
                    Z1=rd.Z1,
                    s=rd.s,
                    t_u=rd.t_u
                )
            case 1:
                responsemessage = sdzkp_pb2.Response(
                    sgdid=self.instance_id,
                    roundid=round_id,
                    Z2=rd.Z2,
                    s=rd.s,
                    t_r=rd.t_r
                )
            case 2:
                responsemessage = sdzkp_pb2.Response(
                    sgdid=self.instance_id,
                    roundid=round_id,
                    Z1=rd.Z1,
                    Z2=rd.Z2
                )
            case _:
                print("Error in challenge, abort")
                return None, None

        verificationresultmessage = self.grpc_stub.Verify(responsemessage)
        return verificationresultmessage.roundresult, verificationresultmessage.verificationresult

    def run_round(self, round_id):
        """
        Executes a single round of the ZKP protocol.

        Parameters:
            round_id (int): The ID of the round.
        """
        c = self.commit(round_id)
        rr, zkpr = self.response(round_id, c)
        print(f"Round result: {rr} ZKP result: {zkpr}")

    def run(self):
        """
        Runs the entire ZKP protocol for the specified number of rounds.
        """
        if self.setup():
            for i in range(self.number_of_rounds):
                self.run_round(i)
