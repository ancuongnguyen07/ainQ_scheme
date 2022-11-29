from dataclasses import dataclass
import EC_operation as ec
from random import randint
from common_parameters import Parameters
from typing import List
from drone import Drone
from EC_operation import ECCPoint

@dataclass
class Leader(Drone):
    '''Class holding a team leader drone'''
    # x_i: int # secret value
    # P_i: ec.ECCPoint # public key

    K_g: int # group key
    l_k: int # random number for distributing group key
    V: ECCPoint

    drone_list: List[Drone]

    def __register_drone__(self, edge_drone: Drone):
        '''Append a given drone to its drone list'''
        assert edge_drone != None
        self.drone_list.append(edge_drone)

        # re-generate a new group key whenever a new drone is added


    def __remove_key__(self, id: str):
        '''Remove a drone with a given id'''
        assert id != ''
        for drone in self.drone_list:
            if drone.id == id:
                self.drone_list.remove(drone)

                # re-generate a new group key whenever an existing drone is removed

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

    def __gen_group_key__(self, common_para: Parameters, t: int):
        '''
        Run by team leader
        Generate a symmetric group session key
        '''
        q,G,H0,H1,P_pub = [common_para.q, common_para.G, common_para.H0,
                        common_para.H1,common_para.P_pub]

        # ----- STEP 1
        K_g = randint(0,q)
        l_k = randint(0,q)

        self.K_g = K_g
        self.l_k = l_k

        # ----- STEP 2
        V = G.__rmul__(l_k)
        self.V = V

        cipher_lists = {}

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
            cipher_lists[drone] = C_i

        return V, cipher_lists

    def __re_key__(self, common_para: Parameters, new_drone: Drone, t: int):
        '''Re-generate group key whenever a new drone join or an
        existing drone leaves'''

        q,P_pub,H0,H1 = common_para.q, common_para.P_pub,common_para.H0,common_para.H1

        # ----- STEP 1
        temp_key = randint(0,q)
        while K_g != None and temp_key == K_g:
            temp_key = randint(0,q)
        K_g = temp_key

        # ----- STEP 2
        if new_drone != None:
            R_i, P_i = new_drone.R_i, new_drone.P_i
            h0_hash_feed = ','.join(list(map(str, [new_drone.id,R_i,P_i])))
            Y_i = P_i.__add__(R_i.__add__(P_pub.__rmul__(H0(h0_hash_feed))))
            T_i = Y_i.__rmul__(self.l_k)

        cipher_list = {}

        # ----- STEP 3
        for drone in self.drone_list:
            h1_hash_feed = ','.join(list(map(str, [self.V,T_i,self.id,self.R_i,self.P_i,
                                                drone.id,drone.R_i,drone.P_i,t])))
            C_i = K_g ^ H1(h1_hash_feed)
            cipher_list[drone] = C_i

        return self.V, cipher_list