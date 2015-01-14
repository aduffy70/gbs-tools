#! /usr/bin/python

# getbarcodecountss.py
# Counts how many reads and bases are assigned to each barcode. Expects a
# fastq file where the samplename (or barcodename) and barcode sequence are
# the last two items in the colon-separated header lines (e.g., the output 
# from trimbarcodes.py).
# Returns:
#   the total number of reads, bases, and unique barcodes in the file, and
#   the number of reads and bases assigned to each barcode      
# Usage: getbarcodecounts.py trimmedfastqdata.fastq headerstartstring

import sys

barcodes = {} # key = barcode and sticky end, value = sample name, readcount, basecount
header_start = sys.argv[2]
header_start_length = len(header_start)
total_read_count = 0
total_base_count = 0

with open(sys.argv[1]) as file: # open the fastqdata file
    fastq_line = 0
    base_count = 0
    sample_name = ""
    barcode = ""
    for line in file:
        if fastq_line == 1: # This is the dataline
            # grab the length
            base_count = len(line) - 1 # Don't count the newline character
            fastq_line = 2
        elif fastq_line == 3: # This is the qualityline
            fastq_line = 0
        elif line[0:len(header_start)] == header_start: # This is the header, the dataline is next
            # grab the samplename and barcode
            header_elements = line.rstrip().split(":") #take off the newline character and then split the colon-separated text. The last 2 elements are the sample name and barcode
            barcode = header_elements[-1]
            sample_name = header_elements[-2]
            fastq_line = 1
        elif line == "+\n": # The quality line is next
            fastq_line = 3
        if fastq_line == 0: # update our counts before we start the next record
            if barcode in barcodes:
                barcodes[barcode][0] = sample_name
                barcodes[barcode][1] += 1
                barcodes[barcode][2] += base_count
            else:
                barcodes[barcode] = [sample_name, 1, base_count]
            total_read_count += 1
            total_base_count += base_count
    print "Barcode,Sample_name,read_count,base_count"
    print "Total,Total,%s,%s" % (total_read_count, total_base_count)
    for key in barcodes.keys():
        print "%s,%s,%s,%s" % (key, barcodes[key][0], barcodes[key][1], barcodes[key][2])
