from random import randint
from random import shuffle
from random import sample
from collections import defaultdict
import re
import datetime
import sys
from GA import *

def encrypt(key, plain):
    L = len(key)
    plain = list(plain) + (L - len(plain) % L)*['X']
    crypt = ['']*len(plain)
    for i in range(len(plain)//L):
        b = i*L
        for j in range(L):
            crypt[b+j] = plain[b + key[j]]
    return "".join(crypt)

if __name__ == "__main__":
    argc =  len(sys.argv) 
    d_flag = False
    input_filename = None
    if argc > 1:
        for arg in sys.argv[1:]:
            if arg == '-d':
                d_flag = True
            else:
                input_filename = arg

    K = 10

    if d_flag == False:
        if input_filename :
            with open(input_filename) as input_file:
                plain = input_file.read()
            if len(plain.split()) < 50 and len(plain.split('_')) < 50:
                fprint("must have > 50 words!") 
                exit(0)
        else:
            plain = input("Enter some plain text below (must have > 50 words ):\n")
            while len(plain.split()) < 50 and len(plain.split('_')) < 50: 
                plain = input("Enter your plain text below (must have > 50 words ):\n")

        plain = re.sub(r'[^A-Z]','_',plain.upper())
        plain = re.sub(r'_+','_',plain)

        fprint("\n\nFormatted plain text:\n{}".format(plain))

        key = list(range(K))
        shuffle(key)
        fprint("\nGenerated a random key:{}".format(key))
        crypt = encrypt(key, plain)
        fprint("\nEncrypted by the key:\n{}\n".format(crypt))

        i = Individual(crypt, key_length = K ,key = key)
        fitness_threshold = i.calcFitness()
        fprint("\nExpected fitness:{}\n".format(fitness_threshold))

    else:
        if input_filename :
            with open(input_filename) as input_file:
                crypt = input_file.read()
        else:
            crypt = input("Enter crypt(Length must be multiple of {}):\n".format(K)).strip()
        if len(crypt) % 10 != 0:
            fprint("Invalid crypt length.")
            exit(0)

        fitness_threshold = 100
        crypt = re.sub(r'[^A-Z]','_',crypt.upper())
        fprint("Your crypt:\n{}\n".format(crypt))

    input("Press Enter to start cracking...")

    d = TranspositionGA(crypt, K)
    d.run(fitness_threshold-1, 100000)
