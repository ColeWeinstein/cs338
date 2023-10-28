#!/usr/bin/env python3
'''
    conversions.py
    Jeff Ondich, 6 May 2022

    Shows how to compute a SHA-256 hash and manipulate the
    relevant Python types.

    Note that when you want to do a new hash, you need to
    call hashlib.sha256() again to get a fresh sha256 object.
'''
import hashlib
import binascii

password = 'moose' # type=string
print(f'password ({type(password)}): {password}')

encoded_password = password.encode('utf-8') # type=bytes
print(f'encodedPassword ({type(encoded_password)}): {encoded_password}')

hasher = hashlib.sha256(encoded_password)
digest = hasher.digest() # type=bytes
print(f'digest ({type(digest)}): {digest}')

digest_as_hex = binascii.hexlify(digest) # weirdly, still type=bytes
print(f'digest_as_hex ({type(digest_as_hex)}): {digest_as_hex}')

digest_as_hex_string = digest_as_hex.decode('utf-8') # type=string
print(f'digest_as_hex_string ({type(digest_as_hex_string)}): {digest_as_hex_string}')

