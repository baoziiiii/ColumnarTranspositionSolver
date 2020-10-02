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
    
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as input_file:
            plain = input_file.read()
        if len(plain.split()) < 50:
            fprint("must have > 50 words!") 
            exit(0)
    else:
        plain = input("Enter some plain text below (must have > 50 words ):\n")
        while len(plain.split()) < 50:
            plain = input("Enter your plain text below (must have > 50 words ):\n")

    plain = re.sub(r'[^A-Z]','_',plain.upper())
    plain = re.sub(r'_+','_',plain)

    fprint("\n\nFormatted plain text:\n{}".format(plain))

    K = 15
    key = list(range(K))
    shuffle(key)
    fprint("\nGenerated a random key:{}".format(key))
    crypt = encrypt(key, plain)
    fprint("\nEncrypted by the key:\n{}\n".format(crypt))

    i = Individual(crypt, key_length = K ,key = key)
    fitness_threshold = i.calcFitness()
    fprint("\nExpected fitness:{}\n".format(fitness_threshold))

    input("Press Enter to start cracking...")

    d = TranspositionGA(crypt, K)
    d.run(fitness_threshold-1, 100000)
