#! /usr/bin/python

# exploreambiguous.py
# When I run sortbarcodes.py I have reads with low distances
# that are equally distant to two or more barcodes so they
# can't be assigned. This script lists those ambiguous
# 12mers and the barcodes that are equally distant. There
# was a question about how we could have reads with a best
# match distance of 2 that could still not be assigned 
# unambiguously if all our barcodes are 4 bases different
# from each other. This script demonstrates how.
# For example, these two barcodes are 4 bases apart but 
# each is only 2 bases different from the example read:
# CTCGTACCAACAATTC - example read 
# ATCGGACCAACAATTC - barcode 1
# CTGATACCAACAATTC - barcode 2
# This version works for reads of any length and can handle
# wobble bases in the cutsite, but does not allow for indels
# when calculating distances between reads and barcodes.

import sys
import operator # for sorting dictionaries

barcodes = {}
min_barcode_length = 100 # Set it bigger than the biggest we expect for now
max_barcode_length = 0 # Set it smaller than the smallest we expect for now
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
with open(sys.argv[1]) as file: # Open the barcode file to make a dictionary and find the range of barcode lengths
    for line in file:
        if line[0] != "#": # Ignore lines starting with a #
            split_line = line.replace(",", " ").split() # allows for comma or space delimited barcode files
            new_barcode = split_line[1].upper() # allows for upper or lowercase barcodes
            barcode_length = len(new_barcode)
            if barcode_length < min_barcode_length:
                min_barcode_length = barcode_length
            elif barcode_length > max_barcode_length:
                max_barcode_length = barcode_length
            barcodes[new_barcode] = split_line[0] # key=barcode sequence, value=barcode name or sample name
# Now we know the range of barcode lengths and can set up the distance lists at the correct length
with open(sys.argv[2]) as file: # Open the 12mer file
    for line in file:
        ambiguous_list = []
        if line[0] != "#":  # Ignore lines starting with a #
            best_match = ""
            best_distance = max_barcode_length + 1 # Start with a value worse than the worst possible match
            split_line = line.split()
            read_count = split_line[1]
            twelvemer = split_line[0]
            for barcode in barcodes:
                distance = 0
                length = len(barcode)
                for x in range(0, length): # Calculate the distance for this barcode
                    if twelvemer[x] not in nucleotides[barcode[x]]: #this accounts for wobble nucleotides in the cutsite
                        distance += 1
                if distance < best_distance: # Best match yet, let's remember this one
                    best_distance = distance
                    best_match = barcode
                    ambiguous_list = [barcode]
                elif distance == best_distance: # Can't choose between 2 best matches
                    best_match = "AMBIGUOUS"
                    ambiguous_list.append(barcode)
            if best_match == "AMBIGUOUS" and best_distance < 5:
                print twelvemer, best_distance,
                for barcode in ambiguous_list:
                    print barcode,
                print ""
