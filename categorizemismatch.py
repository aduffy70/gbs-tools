#! /usr/bin/python

# categorizemismatch.py
# For reads that don't exactly match a barcode, but that 
# are assigned unambiguously, characterize the mismatches
# based on the type of substitution (A to T, G to C, etc.) 
# For each mismatch type, Reports the number of times that 
# substitution type was found in the unique 12mers file and
# the number of reads containing that substitution.
# This version works with any wobble bases in the cutsite.

# Usage: categorizemismatch.py sortbarcodesOUTfile.txt findunique12mersOUT.txt 

import sys
import operator # for sorting dictionaries

mismatch_type_counts = {} # A dictionary with substitution type (AT, GC, etc.) as key and count of mismatches and count of reads as values
                   # The first character in the key is the barcode base (what we assume the base was originally)
reads_per_12mer = {} # A dictionary with unique12mer as key and read count as value
total_12mer_count = 0
ambiguous_12mer_count = 0
unambiguous_12mer_count = 0
comparison_count = 0
mismatch_count = 0
match_count = 0
# Make a dictionary of IUB nucleotide codes so we can handle ANY wobble bases
nucleotides = {"A": "A", "T": "T", "C": "C", "G": "G",
               "R": "GA",
               "K": "GT",
               "S": "GC",
               "W": "AT",
               "M": "AC",
               "Y": "TC",
               "D": "GAT",
               "V": "GAC",
               "B": "GTC",
               "H": "ATC",
               "N": "GATC"}



with open(sys.argv[2]) as file: # open the unique12mers file and make a dictionary to lookup reads per 12mer
    for line in file:
        if line[0] != "#": # ignore lines starting with a #
            split_line = line.split()
            reads_per_12mer[split_line[0]] = int(split_line[1])
with open(sys.argv[1]) as file: # open the sortbarcodesOUT file
    for line in file:
        if line[0] != "#": # Ignore lines starting with a #
            split_line = line.split()
            twelvemer = split_line[0]
            barcode = split_line[1]
            if barcode == "AMBIGUOUS": # we can only compare if we have an unambiguously assigned barcode to compare against
                ambiguous_12mer_count += 1
            else: 
                unambiguous_12mer_count += 1
                for index in range(0,len(barcode)):
                    type = "match"
                    if twelvemer[index] not in nucleotides[barcode[index]]:
                        type = barcode[index] + twelvemer[index]
                    if type != "match":
                        mismatch_count += 1
                        if mismatch_type_counts.has_key(type):
                            mismatch_type_counts[type][0] += 1
                            mismatch_type_counts[type][1] += reads_per_12mer[twelvemer]
                        else: 
                            mismatch_type_counts[type] = [1, reads_per_12mer[twelvemer]]
                    else:
                        match_count += 1
                    comparison_count += 1
            total_12mer_count += 1
print "Total 12mers:", total_12mer_count
print "12mers categorized:", unambiguous_12mer_count
print "Ambiguous 12mers:", ambiguous_12mer_count
print "Bases compared:", comparison_count
print "Mismatched bases:", mismatch_count
print "Matching bases:", match_count
print "Mismatch_type", "Count", "Reads"
for key in mismatch_type_counts:
    print key, mismatch_type_counts[key][0], mismatch_type_counts[key][1] 

                                           

    
