import entity as en
import time
import argparse

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

def drone_partial_key(kgc: en.KGC, drone: en.Drone, sys_para: en.Parameters,verbose: bool):
    '''Assign generated partial key pair by KGC to given Drone'''
    id, P_i = drone.id, drone.P_i
    R_i, s_i = kgc.__gen_partial_key__(sys_para, id, P_i,verbose)
    drone.R_i = R_i
    drone.s_i = s_i

def set_up(kgc: en.KGC, leader: en.Leader, verbose: bool):
    '''Setup and Initialization phase'''

    # ====================== Setup and Initialization
    
    if verbose:
        print()
        print('------------Setup and Initialization Phase------------')
        print()

    ## system parameters of the protocol
    sys_parameters = kgc.__setup__(verbose)

    ## each registered drone runs the GenSecretValue
    q,G = sys_parameters.q, sys_parameters.G
    start = time.time()
    leader.__gen_secret_value__(q, G, verbose)
    end = time.time()
    print(f'GenSecretValue: {end-start:.3f} seconds')

    for edge_drone in leader.drone_list:
        edge_drone.__gen_secret_value__(q, G, verbose)

    ## each registered drone send their identity and public key to the KGC
    ## in order to receive partial private and public keys

    # leader receive partial private and public keys
    drone_partial_key(kgc, leader, sys_parameters,verbose)

    # edge drones receive partial private and public keys
    for edge_drone in leader.drone_list:
        drone_partial_key(kgc, edge_drone, sys_parameters,verbose)

    ## each registered drone runs the GenPrivKey and GenPubKey to generate
    ## a full public/private key pair.

    # ---> Key pairs is accessed by the __full_key_gen__ method in each drone
    # no more code implementation is needed.

    return sys_parameters

def key_gen_retrieval(leader: en.Leader, sys_parameters: en.Parameters,verbose: bool):
    '''Key Generation and Retrieval phase'''

    if verbose:
        print()
        print('------------Key Generation and Retrieval Phase------------')
        print()

    # ====================== Key Generation and Retrieval
    ## random number used for signature authentication
    r1 = leader.__random_number__()
    ## key generation
    t_g = int(time.time())

    start = time.time()
    V, cipher_list = leader.__gen_group_key__(sys_parameters, t_g, verbose)
    end = time.time()

    print(f'GenGroupKey: {end-start:.3f} seconds')
    
    ## sign and verify the message m1
    
    # need to be implemented in a separate file the sign/verify protocol
    mess_to_be_signed = ','.join(list(map(str, [r1,V,leader.K_g])))
    key_retrieval_phase(mess_to_be_signed, V, cipher_list, t_g, leader, sys_parameters, verbose)

    return V, cipher_list

def key_retrieval_phase(mess: str,V, cipher_list,t_g,leader: en.Leader,
                        sys_parameters: en.Parameters, verbose: bool):
    '''
    Team leader send a broadcast message along with the signature
    Each edge drone verify the message using leader's public key
    Then it run key_retrieval algorithm
    '''
    ## sign a message
    signature_r, signature_s = leader.__sign_mess__(mess, sys_parameters)
    if verbose:
        print()
        print('------------Key Retrieval Phase------------')
        print()
        print('Sign and verify digital signature...')
        print(f'Message signature: ({hex(signature_r)},{hex(signature_s)})')
        print('The Leader now sends the broadcast message and the signature to all edge drones...')
        print()

    ## key retrieval
    for edge_drone in leader.drone_list:
        ## verify the signed message
        if verbose:
            en.print_section_separate_head()
            print(f'Drone {edge_drone.id} received the broadcast message')
            print(f'Drone {edge_drone.id} is verifying the signature...')
        is_valid_signature = edge_drone.__verify_mess__(mess, signature_r, signature_s,
                                    leader.P_i, sys_parameters)
        assert is_valid_signature == True
        if verbose:
            print('The signature is valid!')

        start = time.time()
        edge_drone.__key_retrieval__(V,cipher_list,t_g, sys_parameters,verbose)
        end = time.time()
        print(f'KeyRetrieval (drone {edge_drone.id}): {end-start:.3f} seconds')

def group_re_key(kgc: en.KGC, leader: en.Leader, sys_parameters: en.Parameters,
                n: int, verbose: bool):
    '''Group Re-Key phase'''

    if verbose:
        print()
        print('------------Group Re-Key Phase------------')
        en.print_section_separate_head()
        print('New drones join the group...')
        print()

    # ====================== Group Re-Key
    new_drone_list = []
    for _ in range(n):
        ## when a drone joins the group
        new_id = len(leader.drone_list) + 1
        new_drone = en.Edge_Drone(f'{new_id}')
        new_drone.__gen_secret_value__(sys_parameters.q,sys_parameters.G,verbose)

        drone_partial_key(kgc, new_drone, sys_parameters,verbose)

        ## update the group list then run the Re-key algorithms
        leader.__register_drone__(new_drone)
        new_drone_list.append(new_drone)

    r2 = leader.__random_number__()
    t_g = int(time.time())

    start = time.time()
    V, cipher_list = leader.__re_key__(sys_parameters,new_drone_list,t_g,verbose)
    end = time.time()
    print(f'Re_Key: {end-start:.3f} seconds')
    en.print_section_separate_tail()

    ## sign and verify the message m2
    
    # need to be implemented in a separate file the sign/verify protocol
    mess_to_be_signed = ','.join(list(map(str, [r2,V,leader.K_g])))
    key_retrieval_phase(mess_to_be_signed, V, cipher_list, t_g, leader, sys_parameters,verbose)

def main():
    # setting up arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--existing-drone', help='Number of existing edge drones',
                        type=int, required=True, dest='existing_drone')
    parser.add_argument('-n', '--new-drone', help='Number of new drones',
                        type=int, required=True, dest='new_drone')
    parser.add_argument('-v', '--verbose', help='Verbose mode of the script',
                        action='store_true', dest='verbose')

    # parsing arguments
    args = parser.parse_args()
    num_ini_drones = args.existing_drone
    num_new_drones = args.new_drone
    verbose = args.verbose

    # print welcome message if the vebose toggle was switched on
    if verbose:
        print('='*10 + ' Welcome to AinQ protocol using the secp256k1 elliptic curve ' + '='*10)

        print(f'Number of initializing drones: {num_ini_drones}')
        print(f'Number of new drones: {num_new_drones}')

    # starting a protocol
    kgc, leader = initialize_entities(num_ini_drones)
    sys_para = set_up(kgc, leader,verbose)

    key_gen_retrieval(leader, sys_para,verbose)
    group_re_key(kgc, leader, sys_para, num_new_drones, verbose)

if __name__ == '__main__':
    main()