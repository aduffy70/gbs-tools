#! /usr/bin/python

# exploreambiguous.py
# When I run sortbarcodes.py I have 33million reads with
# a best distance of 1 or 2 that are equally distant to
# two or more barcodes so they can't be assigned. This script
# will capture each of those ambiguous 12mers and list which
# barcodes are equally distant so I can see if there is any
# way to salvage those reads. Based on sortbarcodes.py but
# printing just a list of the ambiguous 12mers and their
# closest barcodes. 

# Usage: exploreambiguous.py barcodefile.txt Twelvemerfile.txt

import sys
import operator # for sorting dictionaries

barcodes = {}
distance_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0] # Store the # of unique barcodes with each distance from the best match
barcode_assignments = {}
unambiguous = 0 # count the unambiguously assigned 12mers

with open(sys.argv[1]) as file: # open the barcode file and make a dictionary
    for line in file:
        if line[0] != "#": # Ignore lines starting with a #
            split_line = line.split()
            barcodes[split_line[1]] = split_line[0] # key=barcode, value=sample name
with open(sys.argv[2]) as file: # open the 12mer file
    for line in file:
        if line[0] != "#":  # ignore lines starting with a #
            best_match = ""
            best_distance = 13 # Default value worse than the worst possible match
            split_line = line.split()
            read_count = split_line[1]
            twelvemer = split_line[0]
            elevenmer = split_line[0][0:-1]
            tenmer = split_line[0][0:-2]
            ninemer = split_line[0][0:-3]
            eightmer = split_line[0][0:-4]
            if barcodes.has_key(twelvemer): # exact match
                unambiguous += 1
            elif barcodes.has_key(elevenmer): # exact match
                unambiguous += 1
            elif barcodes.has_key(tenmer): # exact match
                unambiguous += 1
            elif barcodes.has_key(ninemer): # exact match
                unambiguous += 1
            elif barcodes.has_key(eightmer): # exact match
                unambiguous += 1
            else: # try to correct the barcode
                ambiguous_list = []
                for barcode in barcodes:
                    distance = 0
                    length = len(barcode)
                    wobble_site = length - 3 # we will handle the W in the enzyme sticky end differently
                    for x in range(0, length): # calculate the distance for this barcode
                        if x != wobble_site:
                            if twelvemer[x] != barcode[x]:
                                distance += 1
                        else:
                            if twelvemer[x] != "A" and twelvemer[x] != "T":
                                distance += 1
                    if distance < best_distance: # Best match yet
                        best_distance = distance
                        best_match = barcode
                        ambiguous_list = [barcode]
                    elif distance == best_distance: # Can't choose between 2 best matches
                        best_match = "AMBIGUOUS"
                        ambiguous_list.append(barcode)
                if best_match == "AMBIGUOUS" and best_distance < 3:
                    print twelvemer, best_distance,
                    for barcode in ambiguous_list:
                        print barcode,
                    print ""
