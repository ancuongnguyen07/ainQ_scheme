from dataclasses import dataclass
from random import randint
import EC_operation as ec

@dataclass
class Drone:
    id: str
    x_i: int # secret value
    P_i: ec.ECCPoint # public key
    s_i: int # partial secret key
    R_i: ec.ECCPoint # partial public key

    def __gen_secret_value__(self,q,G):
        '''
        Run by each edge drone and a team leader
        Generate a pair of secret/public key for each edge drone d_i or team leader
        '''
        # ---- STEP 1
        # generate a secret key
        x_i = randint(0,q)

        # ---- STEP 2
        # compute corresponding public key
        P_i = G.__rmul__(x_i)

        self.x_i = x_i
        self.P_i = P_i

        return x_i, P_i