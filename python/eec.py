# Source: https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/

def mod_inverse(A, M):
    '''Find the modulo inverse of A over M in the range (0,M)'''
    m0 = M
    y = 0
    x = 1

    if (M == 1):
        return 0

    while (A > 1):

        # q is quotient
        q = A // M

        t = M

        # m is remainder now, process
        # same as Euclid's algo
        M = A % M
        A = t
        t = y

        # Update x and y
        y = x - q * y
        x = t

    # Make x positive
    if (x < 0):
        x += m0

    return x