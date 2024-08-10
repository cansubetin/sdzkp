from sdzkp.sdzkproto import sdzkp_pb2
from sdzkp.sgd import SubgroupDistanceProblem, SubgroupDistanceRound
import random

class Verifier:
    def __init__(self, instance_id) -> None:
        self.instance_id = instance_id

    def handleSetup ( self, sgdinst:sdzkp_pb2.SGDInstance):
       
        self.SGD = SubgroupDistanceProblem.create_from_linearized_generators(sgdinst.generators,sgdinst.m, sgdinst.n, sgdinst.g, sgdinst.min_distance )
        # TODO: Check corner cases and return false if problem is not accepted
        return sdzkp_pb2.SetupAck(sgdid=sgdinst.sgdid, setupresult=True)

    def handleCommit (self, commitments):
        # TODO: Check whether this round is repeated or not!
        rd = SubgroupDistanceRound()
        rd.C1 = commitments.C1
        rd.C2 = commitments.C2
        rd.C3 = commitments.C3
        self.SGD.round_data[commitments.roundid] = rd
        #print(self.instance_id, self.SGD.round_data[commitments.roundid].C1),
        
        c = random.randint(0,2)
        rd.c = c
        return sdzkp_pb2.Challenge(sgdid=commitments.sgdid, roundid = commitments.roundid, challenge=c)
    

    def verify_0 (self, rd:SubgroupDistanceRound, Z1, s, t_u):
        retval = True
        rd.set_seed(s)
        rd.Z1 = Z1
        rd.generate_random_array(self.SGD.n)
        
        rd.U, rd.t_u = self.SGD.H.generate_element_from_bitarray(t_u)
        Z1_minus_R = [a - b for a, b in zip(Z1, rd.R)]
        #print(Z1_minus_R[-20:], rd.U[-20:])
        if Z1_minus_R != rd.U:
            print("Z1_minus_R =? U FAILED")
            retval = False
        else:
            print("Z1_minus_R =? U SUCCEEDED")
            
            expected_C1 = rd.generate_commitment(Z1)
            if rd.C1 != expected_C1:
                print("C1 =? Hash(Z1) FAILED")
                retval = False 
            else:
                print("C1 =? Hash(Z1) SUCCEEDED")

                expected_C3 = rd.generate_commitment(s)
                if expected_C3 != rd.C3:
                    print("C3 =? Hash(s) FAILED")
                    retval = False 
                else:
                    print("C3 =? Hash(s) SUCCEEDED")
                    
        return retval

    def verify_1 (self, rd:SubgroupDistanceRound, Z2, s, t_r):
        retval = True
        rd.set_seed(s)
        rd.Z2 = Z2
        rd.generate_random_array(self.SGD.n)

        rd.r, rd.t_r = self.SGD.H.generate_element_from_bitarray(t_r)
        rd.G = self.SGD.H.multiply_permutations(rd.r,self.SGD.g)

        Z2_minus_R = [a - b for a, b in zip(Z2, rd.R)]
        if Z2_minus_R != rd.G:
            print("Z2_minus_R =? r FAILED")
            retval = False
        else:
            print("Z2_minus_R =? r SUCCEEDED")

            expected_C2 = rd.generate_commitment(Z2)
            if rd.C2 != expected_C2:
                print("C2 =? Hash(Z2) FAILED")
                retval = False 
            else:
                print("C2 =? Hash(Z2) SUCCEEDED")

                expected_C3 = rd.generate_commitment(s)
                if expected_C3 != rd.C3:
                    print("C3 =? Hash(s) FAILED")
                    retval = False 
                else:
                    print("C3 =? Hash(s) SUCCEEDED")

        return retval

    
    def verify_2 (self, rd:SubgroupDistanceRound, Z1, Z2):
        retval = True
        Z1_minus_Z2 = [a - b for a, b in zip(Z1, Z2)]
        #print(Z1[-30:])
        #print(Z2[-30:])
        #print(Z1_minus_Z2[-30:])
        nonzero_count = sum(1 for x in Z1_minus_Z2 if x != 0)
        if nonzero_count > self.SGD.K :
            print("|Z1_minus_Z2<>0| <=? K FAILED", nonzero_count,self.SGD.K )
            retval = False 
        else:
            print("|Z1_minus_Z2<>0| <=? K SUCCEEDED",nonzero_count,self.SGD.K )


            expected_C1 = rd.generate_commitment(Z1)
            if rd.C1 != expected_C1:
                print("C1 =? Hash(Z1) FAILED")
                retval = False 
            else:
                print("C1 =? Hash(Z1) SUCCEEDED")

                expected_C2 = rd.generate_commitment(Z2)
                if rd.C2 != expected_C2:
                    print("C2 =? Hash(Z2) FAILED")
                    retval = False 
                else:
                    print("C2 =? Hash(Z2) SUCCEEDED")

        return retval

    def handleVerify (self, response):
        rd = self.SGD.round_data[response.roundid]
        res = False
        match rd.c:
            case 0:
                #print(0, response.t_u)
                res = self.verify_0(rd, response.Z1, response.s, response.t_u)
            case 1:
                #print(1, response.t_r)
                res = self.verify_1(rd, response.Z2, response.s, response.t_r)
            case 2:
                #print(2)
                res = self.verify_2(rd, response.Z1, response.Z2)
            case _:
                #TODO: Handle corner case for aborting
                print("Error in challenge, abort")
        
        return sdzkp_pb2.VerificationResult(sgdid=response.sgdid, roundid=response.roundid,roundresult=res, verificationresult=True)