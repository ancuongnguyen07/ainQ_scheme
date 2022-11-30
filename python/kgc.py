from dataclasses import dataclass
from random import randint
import EC_operation as ec
import common_parameters as para
import edge_drone as drone

@dataclass
class KGC:
    '''Class holding the KGC entity'''
    
    def __setup__():
        '''
        Run by KGC
        Generate system necessary parameters for cryptographic scheme
        Return a class of Parameters
        '''
        # Code below is provided by course staffs
        # ------ STEP 1
        # Using the secp256k1 elliptic curve equation: yˆ2 = xˆ3 + 7
        # Prime of the finite field
        # Necessary parameters for the cryptographic operations
        P: int = (
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        )

        field = ec.PrimeGaloisField(prime=P)

        A: int = 0
        B: int = 7

        curve256k1 = ec.EllipticCurve(
            a=A,
            b=B,
            field=field
        )   

        I = ec.ECCPoint(x = None, y = None, curve = curve256k1)    # where I is a point at Infinity

        # Generator point of the chosen group
        G = ec.ECCPoint(
            x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
            curve = curve256k1
        )

        # Order of the group generated by G, such that nG = I
        q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

        # ----- STEP 2 + 3
        # master sercret key x and public key P_pub
        x = randint(0, q)
        P_pub = G.__rmul__(x)

        # ----- STEP 4
        # I implement a hash function in a separate file: hash_func.py
        H0 = hash.HASH_FUNC_DICT['H0']
        H1 = hash.HASH_FUNC_DICT['H1']

        # package all parameters into a class holder
        common_para = para.Parameters(x,G,q,P_pub,H0,H1,I,P)

        return common_para

    def __gen_partial_key__(common_para: para.Parameters,
                            d_i: drone.Edge_Drone,P_i: ec.ECCPoint):
        '''
        Run by KGC
        Generate a partial key pair for each drone d_i
        Return R_i, s_i
        '''
        x,q,G,H0 = common_para.x, common_para.q, common_para.G, common_para.H0

        # ---- STEP 1
        # choose a secret value
        r_i = randint(0,q)

        # ---- STEP 2
        # partial public key
        R_i = G.__rmul__(r_i)

        # ---- STEP 3
        # partial secret key
        hash_feed = ','.join(list(map(str, [d_i, R_i, P_i])))
        s_i = r_i + x*H0(hash_feed) % q

        # save R_i and s_i into variables of class Edge_Drone d_i
        d_i.s_i = s_i
        d_i.R_i = R_i

        return R_i, s_i 