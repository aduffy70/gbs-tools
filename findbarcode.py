#!/usr/bin/python

# findbarcode.py
# Looks for a specific hardcoded barcode (or any sequence really) in a fastq file 
# (anywhere within the read) and returns the fastq record for each read containing 
# the barcode, with the index where the barcode was found appended to the description.
# Also returns a count of how many records contained the barcode.
# Note - if for some reason, the descriptions contain sequence info this script 
# may have issues.
# usage: ./findbarcode.py fastqfile.fastq

import sys
import re

barcode1 = "GATCCTGC" # Barcodes to be searched 
barcode2 = "GATCCAGC"
line_count = 0
barcode_count = 0
found = 0
lastline = ""
with open(sys.argv[1]) as file:
    for line in file:
        line_count += 1
        if found == 1: # This is the marker line
            print line,
            found = 2
        elif found == 2: # This is the quality line
            print line,
            found = 0
        elif barcode1 in line: # Look for barcode 1
            index = line.index(barcode1)
            barcode_count += 1
            print lastline[0:-1] + ":" + str(index) # Append the index to the description line
            #print line_count,
            print line,
            found = 1
        elif barcode2 in line: # Look for barcode 2
            index = line.index(barcode2)
            barcode_count += 1
            print lastline[0:-1] + ":" + str(index) # Append the index to the description line
            #print line_count,
            print line,
            found = 1
        lastline = line
print "# Matches found:", barcode_count

