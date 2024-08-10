from sdzkp.max2sat import Max2SAT
from sdzkp.sgd import SubgroupDistanceProblemWithSolution, SubgroupDistanceRound
from sdzkp.sdzkproto import sdzkp_pb2


class Prover:
    def __init__(self, grpc_stub, instance_id, number_of_rounds, num_variables):
        self.grpc_stub = grpc_stub
        self.instance_id = str(instance_id)
        self.number_of_rounds = number_of_rounds
        max2satinstance = Max2SAT(num_variables=num_variables)
        max2satinstance.generate_instance_motoki() #.create_default() # 
        self.SGD = SubgroupDistanceProblemWithSolution(max2satinstance)


    def setup(self):
        linearized_generators = self.SGD.linearize_generators()
        sgdinstance = sdzkp_pb2.SGDInstance(sgdid = self.instance_id, g=self.SGD.g, n=self.SGD.n, m=self.SGD.H.m, generators=linearized_generators, min_distance=self.SGD.K, number_of_rounds=self.number_of_rounds)
        setupackmessage:sdzkp_pb2.SetupAck = self.grpc_stub.Setup(sgdinstance)
        # TODO: Check if problemid is the same!
        return setupackmessage.setupresult


    def commit(self, round_id):
        rd:SubgroupDistanceRound = self.SGD.setup_sdzkp_round(round_id)        
        commitmsg = sdzkp_pb2.Commitments(sgdid=self.instance_id,roundid=round_id,C1=rd.C1, C2=rd.C2, C3=rd.C3)
        challengemessage:sdzkp_pb2.Challenge = self.grpc_stub.Commit(commitmsg)
        # TODO: Check if problemid, roundid are the same, respectively!
        return challengemessage.challenge
    
    def response(self, round_id, c):
        rd:SubgroupDistanceRound = self.SGD.round_data[round_id]
        # TODO: check if rd is none
        # TODO: Check if problemid, roundid are the same, respectively!
        responsemessage = None
        match c:
            case 0:
                responsemessage = sdzkp_pb2.Response(sgdid=self.instance_id, roundid=round_id, Z1=rd.Z1,  s=rd.s,  t_u=rd.t_u)
            case 1:
                responsemessage = sdzkp_pb2.Response(sgdid=self.instance_id, roundid=round_id, Z2=rd.Z2, s=rd.s, t_r=rd.t_r )
            case 2:
                responsemessage = sdzkp_pb2.Response(sgdid=self.instance_id, roundid=round_id, Z1=rd.Z1, Z2=rd.Z2)
            case _:
                #TODO: Handle corner case for aborting
                print("Error in challenge, abort")
        verificationresultmessage:sdzkp_pb2.VerificationResult = self.grpc_stub.Verify(responsemessage)
        return verificationresultmessage.roundresult, verificationresultmessage.verificationresult
    

    def run_round(self, round_id):
        c = self.commit(round_id)
        rr, zkpr = self.response(round_id, c)
        print(f"Round result: {rr} ZKP result: {zkpr}")

    def run(self):
        if self.setup(): # Setup operations by the prover
            for i in range(self.number_of_rounds):
                self.run_round( i)


