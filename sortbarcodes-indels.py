#! /usr/bin/python

# sortbarcodes-indels.py
# Takes a list of unique "12mers" and finds the best matching
# barcode/cutsite for each. This version allows for indels when 
# calculating distance but cannot handle "wobble" bases in the 
# cutsite (R, W, etc).  
# Note: "12mers" can actually be any length.
# Start with a list of unique 12mer sequences cut from GBS fastq 
# data and the number of reads that begin with that 12mer.
# Start with a list of the Samples and Barcodes+enzyme_sticky_end 
# used (space, tab, or comma delimited).
# For each unique 12mer sequence, calculate its distance to the 
# most similar barcode(s). Distance is the count of differing bases
# and indels (levenshtein distance).
# If there is a clear "best" match barcode, return that, 
# otherwise "AMBIGUOUS".
# Output is:
# 1) For each unique 12mer, which barcode was the best match (or
#    "AMBIGUOUS" if there is more than one) and the distance 
# 2) For each possible distance, the number of unambiguous 
#    best matches that had that distance, and the number of reads
# 3) For each barcode, the number of 12mers and reads assigned 
#    with a distance <= 2
# Usage: sortbarcodes.py barcodefile.txt uniquetwelvemerfile.txt

import sys
import operator # for sorting dictionaries
import Levenshtein # for calculating distances allowing for indels

barcodes = {}
barcode_assignments = {}
min_barcode_length = 100 # Set it bigger than the biggest we expect for now
max_barcode_length = 0 # Set it smaller than the smallest we expect for now
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
            whatevermer = twelvemer 
            found_match = 0
            # First we look for exact matches, checking for all possible lengths of barcode
            while (len(whatevermer) >= min_barcode_length) and (found_match == 0):
                if barcodes.has_key(whatevermer): # We found an exact match
                    best_match = whatevermer
                    best_distance = 0
                    found_match = 1
                else: # We didn't find an exact match so we will shorten the whatevermer by 1bp and try again
                    whatevermer = whatevermer[:-1]
            if found_match == 0: # We didn't find an exact match so we look for the least distance barcode
                for barcode in barcodes:
                    # Let's calculate distance using 3 methods and use the lowest
                    # 1) The old, base-by-base comparison (this will score best if there are substituions)
                    # 2) Levenstein distance using a sequence of exact matching length (this will score best if there are insertions) 
                    # 3) Levenstein distance using a sequence of barcode_length + 1 (this will score best if there are deletions)
                    # This is optimized to find single indels of 1bp. Any more than that puts us at a distance of 2 or more anyway.
                    length = len(barcode)
                    distance1 = 0
                    for x in range(0, length):
                        if twelvemer[x] != barcode[x]:
                            distance1 += 1
                    distance2 = Levenshtein.distance(barcode, twelvemer[:length])
                    if max_barcode_length - length > 1:
                        whatevermer = twelvemer[:length + 1]
                    else:
                        whatevermer = twelvemer
                    distance3 = Levenshtein.distance(barcode, whatevermer)
                    distance = min((distance1, distance2, distance3)) # Use the lowest of the 3 distances
                    if distance < best_distance: # Best match yet, let's remember this one
                        best_distance = distance
                        best_match = barcode
                    elif distance == best_distance: # Can't choose between 2 best matches
                        best_match = "AMBIGUOUS"
            print twelvemer, best_match, best_distance # Output
            if best_match != "AMBIGUOUS": # Update counts of 12mers and reads at each distance
                distance_counts[best_distance] += 1
                distance_read_totals[best_distance] += int(read_count)
            if best_distance < 3: # Update counts of 12mers and reads assigned to each barcode
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
