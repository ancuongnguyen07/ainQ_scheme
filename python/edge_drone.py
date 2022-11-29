from dataclasses import dataclass
from drone import Drone

@dataclass
class Edge_Drone(Drone):
    '''Class holding edge drone'''

    def __full_key_gen__(self):
        '''
        Run by each edge drone
        Generate full key pair for each drone
        in the format: (partial_key, key)
        '''
        assert self.R_i != None
        assert self.P_i != None
        assert self.x_i != None
        assert self.s_i != None

        # full private key
        full_priv_key = (self.s_i, self.x_i)

        # full public key
        full_pub_key = (self.R_i, self.P_i)

        return full_priv_key, full_pub_key

    def __key_retrieval__():
        '''Run by each edge drone d_i'''