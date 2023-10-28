'''
    passwords.py
    Written by Cole Weinstein for Carleton College's CS338 course,
    Computer Security.

    Allows a user to crack a specific list of one-word passwords,
    two-word passwords, or salted one-word passwords.

    Example usage: python3 passwords.py 1 to crack the list of
    passwords in passwords1.txt.
'''

import sys
import hashlib
import binascii
import time
import random

def compute_one_word_hashes():
    words = [line.strip().lower() for line in open('words.txt')]
    hashes = {}
    count = 0
    for word in words:
        hash_digest = hashlib.sha256(word.encode('utf-8')).digest()
        digest_str = binascii.hexlify(hash_digest).decode('utf-8')
        hashes[digest_str] = word
        count += 1
    return (hashes, count)

def crack_one_word_passwords():
    start_time = time.time()
    result = compute_one_word_hashes()
    hash_time = time.time()
    hashes, hash_count = result[0], result[1]
    print("Number of hashes computed: {0}\nTotal time to compute hashes: {1:.10f}\nTime per hash: {2:.10f}\n".format(hash_count, hash_time - start_time, (hash_time - start_time) / hash_count))
    
    pass_file = open("passwords1.txt", "r")
    cracked_file = open("cracked1.txt", "w")
    
    cracked_count = 0
    for line in pass_file:
        split_line = line.split(":")
        cracked_file.write(split_line[0] + ":" + hashes[split_line[1]] + "\n")
        cracked_count += 1
    cracked_time = time.time()
    print("Number of passwords cracked: {0}\nTotal time to crack passwords: {1:.10f}\nTime per crack: {2:.10f}\nNumber of passwords cracked per hash computed: {3:.10f}\n".format(cracked_count, cracked_time - hash_time, (cracked_time - hash_time) / cracked_count, cracked_count / hash_count))
    pass_file.close()
    cracked_file.close()

def crack_two_word_passwords():
    prefixes = [line.strip().lower() for line in open('words.txt')]
    random.shuffle(prefixes)
    prefixes.insert(0, "")
    suffixes = [line.strip().lower() for line in open('words.txt')]
    
    stored_hashes = {}
    with open("passwords2.txt", "r") as pass_file:
        for line in pass_file:
            username, pass_hash = tuple(line.split(":")[:2])
            stored_hashes[pass_hash] = username 

    hash_count, cracked_count = 0, 0
    cracked_file = open("cracked2.txt", "w")

    start_time = time.time()
    end_time = time.time()
    for pre in prefixes:
        for suf in suffixes:
            password = pre + suf
            hash_digest = hashlib.sha256(password.encode('utf-8')).digest()
            digest_str = binascii.hexlify(hash_digest).decode('utf-8')
            hash_count += 1
            try:
                print(stored_hashes[digest_str] + ":" + password + "\n")
                cracked_file.write(stored_hashes[digest_str] + ":" + password + "\n")
                cracked_count += 1
            except KeyError as error:
                pass

        end_time = time.time()
        if (end_time - start_time > 1800):
            break
    
    print("Number of hashes computed: {0}\nAverage time per hash computed: {1:.10f}\nNumber of passwords cracked: {2}\nAverage time per password cracked: {3:.10f}\nTotal time elapsed: {4:.10f}\nNumber of passwords cracked per hash computed: {5:.10f}\n".format(hash_count, (end_time - start_time) / hash_count, cracked_count, (end_time - start_time) / cracked_count, end_time - start_time, cracked_count / hash_count))

    cracked_file.close()

def compute_salted_one_word_hash(words, salt, hash):
    hash_start_time = time.time()
    count = 0
    for word in words:
        salted_word = salt + word
        hash_digest = hashlib.sha256(salted_word.encode('utf-8')).digest()
        digest_str = binascii.hexlify(hash_digest).decode('utf-8')
        count += 1
        if (digest_str == hash):
            return (word, count, time.time() - hash_start_time)
    return ("", count, time.time() - hash_start_time)

def crack_salted_one_word_passwords():
    start_time = time.time()

    print("hello")
    
    words = [line.strip().lower() for line in open('words.txt')]
    pass_file = open("passwords3.txt", "r")
    cracked_file = open("cracked3.txt", "w")
    
    cracked_count, hash_count, hashing_time = 0, 0, 0
    for line in pass_file:
        split_line = line.split(":")
        password_data = split_line[1].split("$")
        result = compute_salted_one_word_hash(words, password_data[2], password_data[3])
        if (result[0] != ""):
            cracked_file.write(split_line[0] + ":" + result[0] + "\n")
            cracked_count += 1
            print(split_line[0] + ":" + result[0] + " | " + (str)(cracked_count))
        hash_count += result[1]
        hashing_time += result[2]
    cracked_time = time.time()
    print("Number of hashes computed: {0}\nTotal time to compute hashes: {1:.10f}\nAverage time per hash computed: {2:.10f}\nNumber of passwords cracked: {3}\nTotal time to crack passwords: {4:.10f}\nTime per crack: {5:.10f}\nNumber of passwords cracked per hash computed: {6:.10f}\n".format(hash_count, hashing_time, hashing_time / hash_count, cracked_count, cracked_time - start_time, (cracked_time - start_time) / cracked_count, cracked_count / hash_count))
    pass_file.close()
    cracked_file.close()


def main():
    if (len(sys.argv) < 2):
        print("Argument Error: no cracking intention specified.\n")
        exit(1)

    for item in sys.argv:
        print(item + "\n")
    
    if ((int) (sys.argv[1]) == 1):
        crack_one_word_passwords()
    elif ((int) (sys.argv[1]) == 2):
        crack_two_word_passwords()
    elif ((int) (sys.argv[1]) == 3):
        crack_salted_one_word_passwords()

if __name__ == "__main__":
    main()