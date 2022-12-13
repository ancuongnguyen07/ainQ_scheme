import entity as en
import time

def initialize_entities(n):
    '''Create involving entities: KGC, team leader, `n` number of edge drones'''
    # create a new KGC entity
    kgc = en.KGC()

    # create a team leader
    leader = en.Leader('leader A')

    # create a list of n edge drones
    for i in range(n):
        id = f'{i+1}'
        new_drone = en.Edge_Drone(id=id)
        leader.__register_drone__(new_drone)

    return kgc, leader

def drone_partial_key(kgc: en.KGC, drone: en.Drone, sys_para: en.Parameters):
    '''Assign generated partial key pair by KGC to given Drone'''
    id, P_i = drone.id, drone.P_i
    R_i, s_i = kgc.__gen_partial_key__(sys_para, id, P_i)
    drone.R_i = R_i
    drone.s_i = s_i

def set_up(kgc: en.KGC, leader: en.Leader):
    '''Setup and Initialization phase'''

    # ====================== Setup and Initialization
    
    ## system parameters of the protocol
    sys_parameters = kgc.__setup__()

    ## each registered drone runs the GenSecretValue
    q,G = sys_parameters.q, sys_parameters.G
    # start = time.time()
    leader.__gen_secret_value__(q, G)
    # end = time.time()
    # print(f'GenSecretValue: {end-start:.3f} s')

    for edge_drone in leader.drone_list:
        edge_drone.__gen_secret_value__(q, G)

    ## each registered drone send their identity and public key to the KGC
    ## in order to receive partial private and public keys

    # leader receive partial private and public keys
    drone_partial_key(kgc, leader, sys_parameters)

    # edge drones receive partial private and public keys
    for edge_drone in leader.drone_list:
        drone_partial_key(kgc, edge_drone, sys_parameters)
        id = edge_drone.id
        # en.print_section_separate_head()
        # print(f"Drone {id}'s Partial Secret key: {edge_drone.s_i}")
        # print(f"Drone {id}'s Partial Public key: {edge_drone.R_i}")
        # en.print_section_separate_tail()

    ## each registered drone runs the GenPrivKey and GenPubKey to generate
    ## a full public/private key pair.

    # ---> Key pairs is accessed by the __full_key_gen__ method in each drone
    # no more code implementation is needed.

    return sys_parameters

def key_gen_retrieval(leader: en.Leader, sys_parameters: en.Parameters):
    '''Key Generation and Retrieval phase'''

    # ====================== Key Generation and Retrieval
    ## random number used for signature authentication
    r1 = leader.__random_number__()
    ## key generation
    t_g = int(time.time())

    # start = time.time()
    V, cipher_list = leader.__gen_group_key__(sys_parameters, t_g)
    # end = time.time()

    # print(f'GenGroupKey: {end-start:.3f}')
    
    ## sign and verify the message m1
    
    # need to be implemented in a separate file the sign/verify protocol
    mess_to_be_signed = ','.join(list(map(str, [r1,V,leader.K_g])))
    sign_and_verify(mess_to_be_signed, V, cipher_list, t_g, leader, sys_parameters)

    return V, cipher_list

def sign_and_verify(mess: str,V, cipher_list,t_g,leader: en.Leader, sys_parameters: en.Parameters):
    '''
    Team leader send a broadcast message along with the signature
    Each edge drone verify the message using leader's public key
    Then it run key_retrieval algo
    '''
    ## sign a message
    # signature_r, signature_s = leader.__sign_mess__(mess, sys_parameters)

    ## key retrieval
    for edge_drone in leader.drone_list:
        ## verify the signed message
        # is_valid_signature = edge_drone.__verify_mess__(mess, signature_r, signature_s,
        #                             leader.P_i, sys_parameters)
        # assert is_valid_signature == True
        # start = time.time()
        edge_drone.__key_retrieval__(V,cipher_list,t_g, sys_parameters)
        # end = time.time()
        # print(f'KeyRetrieval: {end-start:.3f} s')

def group_re_key(kgc: en.KGC, leader: en.Leader, sys_parameters: en.Parameters, n: int):
    '''Group Re-Key phase'''

    # ====================== Group Re-Key
    new_drone_list = []
    for _ in range(n):
        ## when a drone joins the group
        new_id = len(leader.drone_list) + 1
        new_drone = en.Edge_Drone(f'drone {new_id}')
        new_drone.__gen_secret_value__(sys_parameters.q,sys_parameters.G)

        drone_partial_key(kgc, new_drone, sys_parameters)

        ## update the group list then run the Re-key algorithms
        leader.__register_drone__(new_drone)
        new_drone_list.append(new_drone)

    r2 = leader.__random_number__()
    t_g = int(time.time())

    # start = time.time()
    V, cipher_list = leader.__re_key__(sys_parameters,new_drone_list,t_g)
    # end = time.time()
    # print(f'Re_Key: {end-start:.3f}')

    ## sign and verify the message m2
    
    # need to be implemented in a separate file the sign/verify protocol
    mess_to_be_signed = ','.join(list(map(str, [r2,V,leader.K_g])))
    sign_and_verify(mess_to_be_signed, V, cipher_list, t_g, leader, sys_parameters)

def main():
    print('='*10 + ' Welcome to AinQ protocol using the secp256k1 elliptic curve ' + '='*10)

    num_ini_drones = 1

    # print(f'Number of existing drones: {num_ini_drones}')
    num_new_drones = 1
    # print(f'Number of new drones: {num_new_drones}')

    kgc, leader = initialize_entities(num_ini_drones)
    sys_para = set_up(kgc, leader)

    key_gen_retrieval(leader, sys_para)
    group_re_key(kgc, leader, sys_para, num_new_drones)

if __name__ == '__main__':
    main()