from dataclasses import dataclass
from random import randint
import EC_operation as ec
import common_parameters as para

@dataclass
class Leader:
    x_i: int
    P_i: ec.ECCPoint

    def __gen_secret_value__(self,common_para: para.Parameters):
        '''
        Run by each edge drone and a team leader
        Generate a pair of secret/public key for each edge drone d_i or team leader
        Return x_i, P_i
        '''
        q,G = common_para.q, common_para.G

        # ---- STEP 1
        # generate a secret key
        x_i = randint(0,q)

        # ---- STEP 2
        # compute corresponding public key
        P_i = G.__rmul__(x_i)

        self.P_i = P_i
        self.x_i = x_i

        return x_i, P_i