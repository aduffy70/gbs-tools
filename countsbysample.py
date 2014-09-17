#! /usr/bin/python

# countsbysample.py
# Take my corrected and trimmed fastq file and count how many of the sequences
# are from each sample/barcode. Expects to find the sample name  and barcode 
# at the end of the dataline separated by colons: 
# @HISEQ blahblah:blah:sample:barcode
# Returns a list of Sample-barcodes and read counts sorted by reads.
# Usage: correctbarcodes.py fastqdata.fastq 

import sys
import operator

samples = {} # A dictionary of samples/barcodes and counts
total_read_count = 0

with open(sys.argv[1]) as file: # open the fastqdata file
    for line in file:
        if line[0:6] == "@HISEQ": # This is the header
            header_elements = line.split(":")
            sample_barcode = header_elements[-2] + "-" + header_elements[-1]
            sample_barcode = sample_barcode[0:-1] # drop the newline char
            if samples.has_key(sample_barcode):
                samples[sample_barcode] += 1
            else:
                samples[sample_barcode] = 1
            total_read_count += 1
print "Sample-barcode", "reads"
sorted_samples = sorted(samples.iteritems(), key=operator.itemgetter(1), reverse=True)
for item in sorted_samples:
    print item[0], item[1]
print "Samples-barcodes:", len(sorted_samples)
print "Total Reads:", total_read_count
