#! /usr/bin/python

# sortbarcodes-wobble.py
# Takes a list of unique "12mers" and finds the best matching
# barcode/cutsite for each. This version allows for "wobble"
# bases in the cutsite (R, W, etc) but does not allow for
# indels when calculationg the distance.
# Note: "12mers" can actually be any length.
# Start with a list of unique 12mer sequences cut from GBS fastq 
# data and the number of reads that begin with that 12mer.
# Start with a list of the Samples and Barcodes+enzyme_sticky_end 
# used (space, tab, or comma delimited).
# For each unique 12mer sequence, calculate its distance to the 
# most similar barcode(s). Distance is the count of differing bases.
# If there is a clear "best" match barcode, return that, 
# otherwise "AMBIGUOUS".
# Output is:
# 1) For each unique 12mer, which barcode was the best match (or  
#    "AMBIGUOUS" if there is more than one) and the distance
# 2) For each possible distance, the number of unambiguous 
#    best matches that had that distance, and the number of reads
# 3) For each barcode, the number of 12mers and reads assigned 
#    with a distance <= 2
# Usage: sortbarcodes.py barcodefile.txt Twelvemerfile.txt

import sys
import operator # for sorting dictionaries

barcodes = {}
barcode_assignments = {}
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
            barcode_assignments[new_barcode] = [0, 0] # key=barcode, value=[12mers assigned, reads assigned]
    barcode_assignments["AMBIGUOUS"] = [0, 0] # We need a place to record how many 12mers and reads couldn't be assigned
# Now we know the range of barcode lengths and can set up the distance lists at the correct length
distance_counts = [0] * (max_barcode_length + 1) # stores the # of unique barcodes with each distance from the best match
distance_read_totals = [0] * (max_barcode_length + 1) # stores the # of reads with each distance from the best match 
with open(sys.argv[2]) as file: # Open the 12mer file
    for line in file:
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
                elif distance == best_distance: # Can't choose between 2 best matches
                    best_match = "AMBIGUOUS"
            print twelvemer, best_match, best_distance # Output
            if best_match != "AMBIGUOUS":
                distance_counts[best_distance] += 1
                distance_read_totals[best_distance] += int(read_count)
            if best_distance < 3:
                barcode_assignments[best_match][0] += 1
                barcode_assignments[best_match][1] += int(read_count)
    # Print counts of 12mers and reads at each distance
    print "# Distance - Unique 12mers - Total reads (unambiguously assigned)"
    for x in range(0, max_barcode_length + 1):
        print "# ", x, distance_counts[x], distance_read_totals[x]
    # Print counts of 12mers and reads assigned to each barcode
    print "# Barcode - 12mers assigned - Total reads (with distance 2 or less)"
    for barcode in barcode_assignments:
        print "# ", barcode, barcode_assignments[barcode][0], barcode_assignments[barcode][1]
