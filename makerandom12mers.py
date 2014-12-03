#! /usr/bin/python

# makerandom12mers.py
# Generates a fastq file with a specified number of random sequences of a
# specified length.
# Used this to increase my confidence that the results of my barcode matching
# process are not just what might be expected by chance in a large dataset.
# usage: ./makerandom12mers.py number_of_sequences length_of_sequences

import random
import sys

bases = ["G", "A", "T", "C"]
for sequence in range(0, int(sys.argv[1])):
    new_sequence = ""
    for base in range(0, int(sys.argv[2])):
        new_sequence += random.choice(bases)
    print "@HISEQ-Dummyheader"
    print new_sequence
    print "+"
    print "DUMMYQUALITY"
        
