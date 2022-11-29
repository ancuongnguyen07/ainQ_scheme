from dataclasses import dataclass
import EC_operation as ec
import types

@dataclass
class Parameters:
    '''Class holding common parameters of the AinQ scheme'''

    x: int
    G: ec.ECCPoint
    q: int
    P_pub: ec.ECCPoint
    H0: types.FunctionType
    H1: types.FunctionType
    I: ec.ECCPoint
    P: int