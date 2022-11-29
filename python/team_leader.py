from dataclasses import dataclass
from random import randint
import EC_operation as ec
import common_parameters as para
import edge_drone as drone
from typing import List

@dataclass
class Leader(drone.Edge_Drone):
    '''Class holding a team leader drone'''
    # x_i: int # secret value
    # P_i: ec.ECCPoint # public key

    drone_list: List[drone.Edge_Drone]

    def __register_drone__(self, edge_drone: drone.Edge_Drone):
        '''Append a given drone to its drone list'''
        assert edge_drone != None
        self.drone_list.append(edge_drone)

    # def __gen_secret_value__(self,common_para: para.Parameters):
    #     '''
    #     Run by each edge drone and a team leader
    #     Generate a pair of secret/public key for each edge drone d_i or team leader
    #     Return x_i, P_i
    #     '''
    #     q,G = common_para.q, common_para.G

    #     # ---- STEP 1
    #     # generate a secret key
    #     x_i = randint(0,q)

    #     # ---- STEP 2
    #     # compute corresponding public key
    #     P_i = G.__rmul__(x_i)

    #     self.P_i = P_i
    #     self.x_i = x_i

    #     return x_i, P_i

    def gen_group_key(self, common_para: para.Parameters, t: int):
        '''
        Run by team leader
        Generate a symmetric group session key
        '''
        q,G,H0,H1,P_pub = [common_para.q, common_para.G, common_para.H0,
                        common_para.H1,common_para.P_pub]

        # ----- STEP 1
        K_g = randint(0,q)
        l_k = randint(0,q)

        # ----- STEP 2
        V = G.__rmul__(l_k)

        cipher_lists = []

        for drone in self.drone_list:
            # ----- STEP 3
            R_i, P_i = drone.R_i, drone.P_i

            # ----- STEP 4
            h0_hash_feed = ','.join(list(map(str, [drone.id, R_i, P_i])))
            Y_i = P_i.__add__(R_i.__add__(P_pub.__rmul__(H0(h0_hash_feed))))
            T_i = Y_i.__rmul__(l_k)
            h1_hash_feed = ','.join(list(map(str, [V,T_i,self.id,self.R_i,self.P_i,
                                                drone.id,drone.R_i,drone.P_i,t])))
            C_i = K_g ^ H1(h1_hash_feed)
            cipher_lists.append(C_i)

        return V, cipher_lists