#! /usr/bin/python

# sortbarcodes-zd.py
# A version for Zach's data.
# Making this work for generic gbs data will be difficult!
# Start with a list of unique 12mer sequences (with
# no Ns) cut from GBS fastq data and the number of reads that
# begin with that 12mer.
# Start with a list of the Samples and Barcodes+enzyme_sticky_end 
# used (same format as GBS barcode splitter requires)
# For each unique 12mer sequence, determine whether it is:
#  1) an exact match for a barcode, or
#  2) calculate its distance to the most similar barcode(s)
# Distance is just the count of differing bases.
# If there is a clear "best" match barcode, return that, 
# otherwise "AMBIGUOUS".
# Output is:
# 1) For each unique 12mer, which barcode was the best match 
#    and the distance
# 2) For each possible distance (0-12), the number of unambiguous 
#    best matches that had that distance, and the number of reads
# 3) For each barcode, the number of 12mers and reads assigned 
#    with a distance < 3
# Usage: sortbarcodes.py barcodefile.txt Twelvemerfile.txt

import sys
import operator # for sorting dictionaries

barcodes = {}
distance_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #distance_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0] # Store the # of unique barcodes with each distance from the best match
distance_read_totals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #distance_read_totals = [0,0,0,0,0,0,0,0,0,0,0,0,0]
barcode_assignments = {}

with open(sys.argv[1]) as file: # open the barcode file and make a dictionary
    for line in file:
        if line[0] != "#": # Ignore lines starting with a #
            split_line = line.split(",") # split_line = line.split()
            barcodes[split_line[1]] = split_line[0] # key=barcode, value=sample name
            barcode_assignments[split_line[1]] = [0, 0] # key=barcode, value=[12mers assigned, reads assigned]
        barcode_assignments["AMBIGUOUS"] = [0, 0] # We need a place to record how many 12mers and reads couldn't be assigned
with open(sys.argv[2]) as file: # open the 12mer file
    for line in file:
        if line[0] != "#":  # ignore lines starting with a #
            best_match = ""
            best_distance = 17 #best_distance = 13 # Default value worse than the worst possible match
            split_line = line.split()
            read_count = split_line[1]
# For -zd these are actually 16mers, 15mers, and 14mers but I didn't want to rename all the variables            
            twelvemer = split_line[0]
            elevenmer = split_line[0][0:-1]
            tenmer = split_line[0][0:-2]
            #ninemer = split_line[0][0:-3]
            #eightmer = split_line[0][0:-4]
            if barcodes.has_key(twelvemer): # exact match
                best_match = twelvemer
                best_distance = 0
            elif barcodes.has_key(elevenmer): # exact match
                best_match = elevenmer
                best_distance = 0
            elif barcodes.has_key(tenmer): # exact match
                best_match = tenmer
                best_distance = 0
            #elif barcodes.has_key(ninemer): # exact match
            #    best_match = ninemer
            #    best_distance = 0
            #elif barcodes.has_key(eightmer): # exact match
            #    best_match = eightmer
            #    best_distance = 0
            else: # try to correct the barcode
                for barcode in barcodes:
                    distance = 0
                    length = len(barcode)
                    #wobble_site = length - 3 # we will handle the W in the enzyme sticky end differently
                    for x in range(0, length): # calculate the distance for this barcode
                        #if x != wobble_site:
                            #if twelvemer[x] != barcode[x]:
                                #distance += 1
                        #else:
                        #    if twelvemer[x] != "A" and twelvemer[x] != "T":
                        #        distance += 1
                        if twelvemer[x] != barcode[x]:
                            distance += 1
                    if distance < best_distance: # Best match yet
                        best_distance = distance
                        best_match = barcode
                    elif distance == best_distance: # Can't choose between 2 best matches
                        best_match = "AMBIGUOUS"
            print twelvemer, best_match, best_distance
            if best_match != "AMBIGUOUS":
                distance_counts[best_distance] += 1
                distance_read_totals[best_distance] += int(read_count)
            if best_distance < 3:
                barcode_assignments[best_match][0] += 1
                barcode_assignments[best_match][1] += int(read_count)
    print "# Distance - Unique 12mers - Total reads (unambiguously assigned)"
    for x in range(0, 17): #for x in range(0, 13):
        print "# ", x, distance_counts[x], distance_read_totals[x]
    print "# Barcode - 12mers assigned - Total reads (with distance 2 or less)"
    for barcode in barcode_assignments:
        print "# ", barcode, barcode_assignments[barcode][0], barcode_assignments[barcode][1]

