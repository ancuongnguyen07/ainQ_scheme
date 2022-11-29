from dataclasses import dataclass
from drone import Drone
from EC_operation import ECCPoint
from common_parameters import Parameters
from team_leader import Leader

@dataclass
class Edge_Drone(Drone):
    '''Class holding edge drone'''

    K_g: int # group key
    q_k: Leader # team leader

    def __assign_leader__(self, leader: Leader):
        self.q_k = leader

    def __key_retrieval__(self,V: ECCPoint,cipher_list, common_para: Parameters, t_g):
        '''Run by each edge drone d_i'''
        T_i = V.__rmul__(self.x_i + self.s_i)
        h1_hash_feed = ','.join(list(map(str, [V,T_i,self.q_k.id,self.q_k.R_i,self.q_k.P_i,
                                                self.id,self.R_i,self.P_i,t_g])))
        K_g = cipher_list[self] ^ Parameters.H1(h1_hash_feed)

        self.K_g = K_g
        return K_g
