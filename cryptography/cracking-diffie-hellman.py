"""cracking-diffie-hellman.py

    9/25/2023
    A simple program to crack a Diffie-Hellman exchange done with
    insufficiently small numbers.

    Written by Cole Weinstein for use in Carleton College's CS338.
"""

def find_key(g, p, a, b):
    """Return the integer key agreed on in a Diffie-Hellman exchange with
    insufficiently small modulus.
    
    Parameters g, p, a, and b: public information sent to establish the shared
    secret K.
    Precondition: each of the parameters is an int, and p is relatively small.
    """
    # Find x such that (g ** x) % p = a using brute force.
    for x in range(p):
        if ((g ** x) % p == a):
            print("x = " + str(x))
            break

    # Find y such that (g ** y) % p = b using brute force.
    for y in range(61):
        if ((g ** y) % p == b):
            print("y = " + str(y))
            break

    # Return K = (g ** (x * y)) % p.
    return (g ** (x * y)) % p

def main():
    g, p, a, b = 7, 61, 30, 17
    print("K = " + str(find_key(g, p, a, b)))

if __name__ == "__main__":
    main()