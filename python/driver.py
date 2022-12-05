import entity as en
import time

def main():
    # create a new KGC entity
    kgc = en.KGC()

    # create a team leader
    leader = en.Leader('leader A')

    # create a list of 10 edge drones
    drone_list = []
    for i in range(3):
        id = f'drone {i+1}'
        new_drone = en.Edge_Drone(id=id)
        new_drone.__assign_leader__(leader)
        drone_list.append(new_drone)

    # ====================== Setup and Initialization
    
    ## system parameters of the protocol
    sys_parameters = kgc.__setup__()

    ## each registered drone runs the GenSecretValue
    q,G = sys_parameters.q, sys_parameters.G
    leader.__gen_secret_value__(q, G)
    for edge_drone in drone_list:
        edge_drone.__gen_secret_value__(q, G)

    ## each registered drone send their identity and public key to the KGC
    ## in order to receive partial private and public keys

    # leader receive partial private and public keys
    id_leader, P_i_leader = leader.id, leader.P_i
    R_i_leader, s_i_leader = kgc.__gen_partial_key__(sys_parameters,id_leader,P_i_leader)
    leader.R_i = R_i_leader
    leader.s_i = s_i_leader

    # edge drones receive partial private and public keys
    for edge_drone in drone_list:
        id_drone, P_i_drone = edge_drone.id, edge_drone.P_i
        R_i_drone, s_i_drone = kgc.__gen_partial_key__(sys_parameters,id_drone, P_i_drone)
        edge_drone.R_i = R_i_drone
        edge_drone.s_i = s_i_drone

    leader.drone_list = drone_list

    ## each registered drone runs the GenPrivKey and GenPubKey to generate
    ## a full public/private key pair.

    # ---> Key pairs is accessed by the __full_key_gen__ method in each drone
    # no more code implementation is needed.

    # ====================== Key Generation and Retrieval
    ## random number
    r1 = leader.__random_number__()
    ## key generation
    t_g = int(time.time())
    V, cipher_list = leader.__gen_group_key__(sys_parameters, t_g)

    ## sign and verify the message m1
    
    # need to be implemented in a separate file the sign/verify protocol
    mess_to_be_signed = ','.join(list(map(str, [r1,V,leader.K_g])))
    signature_r, signature_s = leader.__sign_mess__(mess_to_be_signed, sys_parameters)

    ## key retrieval
    for edge_drone in drone_list:
        is_valid_signature = edge_drone.__verify_mess__(mess_to_be_signed, signature_r, signature_s,
                                    leader.P_i, sys_parameters)
        assert is_valid_signature == True
        edge_drone.__key_retrieval__(V,cipher_list,t_g, sys_parameters)

    # ====================== Group Re-Key
    ## when a drone joins or leaves the group
    new_drone = en.Edge_Drone('New drone')
    new_drone.__gen_secret_value__(sys_parameters.q,sys_parameters.G)

    id_drone, P_i_drone = new_drone.id, new_drone.P_i
    R_i_drone, s_i_drone = kgc.__gen_partial_key__(sys_parameters,id_drone, P_i_drone)
    new_drone.R_i = R_i_drone
    new_drone.s_i = s_i_drone

    ## update the group list then run the Re-key algorithms
    leader.__register_drone__(new_drone)
    r2 = leader.__random_number__()
    t_g = int(time.time())
    V, cipher_list = leader.__gen_group_key__(sys_parameters, t_g)

    ## sign and verify the message m2
    
    # need to be implemented in a separate file the sign/verify protocol
    mess_to_be_signed = ','.join(list(map(str, [r2,V,leader.K_g])))
    signature_r, signature_s = leader.__sign_mess__(mess_to_be_signed, sys_parameters)

    ## key retrieval
    for edge_drone in leader.drone_list:
        is_valid_signature = edge_drone.__verify_mess__(mess_to_be_signed, signature_r, signature_s,
                                    leader.P_i, sys_parameters)
        assert is_valid_signature == True
        edge_drone.__key_retrieval__(V,cipher_list,t_g, sys_parameters)


if __name__ == '__main__':
    main()