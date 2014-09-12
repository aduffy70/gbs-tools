#! /usr/bin/python

# doublecheckdups.py
# Make sure my list of unique 12mers is really unique 12mers!
# usage: ./dounlecheckdups.py unique12mers.txt

import sys
import operator # for sorting dictionaries

barcodes = {}
duplicates = 0
total_count = 0
with open(sys.argv[1]) as file: # open the 12mer file
    for line in file:
        if line[0] != "#":  # ignore lines starting with a #
            split_line = line.split()
            read_count = split_line[1]
            twelvemer = split_line[0]
            if barcodes.has_key(twelvemer): # duplicate!!
                print twelvemer, " is a duplicate!!"
                duplicates += 1 
            else :
                barcodes[twelvemer] = split_line[1]
            total_count += 1
    print "Duplicates: ", duplicates
    print "Unique: ", len(barcodes)
    print "Total count: ", total_count
