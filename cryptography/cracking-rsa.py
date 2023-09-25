"""cracking-rsa.py

    9/25/2023
    Implements two tools: 
        1) Find an RSA secret key using brute force given an RSA public key.
        2) Decrypt a ciphertext given the correct RSA private key.

    Written by Cole Weinstein for use in Carleton College's CS338.
"""
from math import floor

def find_private_key(e, n):
    """Return the private key exponent corresponding to a given public key.

    Parameter e: the exponent integer of the public key to be cracked
    Precondition: e is an int, and e < n

    Parameter n: the modulus integer of the public and private keys
    Precondition: n is an int
    """

    # The loop need only iterate over the range 2 to floor(n/2) because 2 is
    # the smallest prime, and the largest factor of n must be less than or
    # equal to n/2.
    for p in range(2, floor(n/2)):
        found_primes = False
        for q in range(2, floor(n/2)):
            if (p * q == n):
                found_primes = True
                break
        if (found_primes == True):
            break

    # By the RSA algorithm, d is computed such that d*e == 1 mod (p-1)*(q-1).
    for d in range(1, (p-1)*(q-1)):
        if ((e * d) % ((p-1) * (q-1)) == 1):
            break
    
    # A short print statement to provide some information to the user.
    print("n = " + str(n) + "\np = " + str(p) + "\nq = " + str(q)
          + "\ne = " + str(e) + "\nd = " + str(d))
    return d

def decrypt_ciphertext(ciphertext, d, n):
    """Return the decrypted text given a ciphertext and RSA private key.
    
    Parameter ciphertext: the ciphertext to be decrypted
    Precondition: ciphertext is a list of ints, where each item is a
    concatenation of two binary ASCII values.

    Parameter d: the exponent integer of the private key to decrypt with
    Precondition: d is an int, and d < n

    Parameter n: the modulus integer of the private key
    Precondition: n is an int
    """
    decrypted_text = ""

    # Each decrypted item is two ASCII characters concatenated.
    for item in ciphertext:
        decrypted_block = (item ** d) % n
        first_char = decrypted_block >> 8
        second_char = decrypted_block % 128
        decrypted_text = decrypted_text + chr(first_char) + chr(second_char)

    return decrypted_text


def main():
    e, n = 17, 170171
    d = find_private_key(e, n)
    
    ciphertext = [65426, 79042, 53889, 42039, 49636, 66493, 41225, 58964,
                  126715, 67136, 146654, 30668, 159166, 75253, 123703, 138090,
                  118085, 120912, 117757, 145306, 10450, 135932, 152073, 141695,
                  42039, 137851, 44057, 16497, 100682, 12397, 92727, 127363,
                  146760, 5303, 98195, 26070, 110936, 115638, 105827, 152109,
                  79912, 74036, 26139, 64501, 71977, 128923, 106333, 126715,
                  111017, 165562, 157545, 149327, 60143, 117253, 21997, 135322,
                  19408, 36348, 103851, 139973, 35671, 93761, 11423, 41336,
                  36348, 41336, 156366, 140818, 156366, 93166, 128570, 19681,
                  26139, 39292, 114290, 19681, 149668, 70117, 163780, 73933,
                  154421, 156366, 126548, 87726, 41418, 87726, 3486, 151413,
                  26421, 99611, 157545, 101582, 100345, 60758, 92790, 13012,
                  100704, 107995]
    print(decrypt_ciphertext(ciphertext, d, n))

if __name__ == "__main__":
    main()