#! /usr/bin/python

# removeemptysequences.py
# After trimming adapters with cutadapt we are left with some empty sequences
# (the read was just an adapter/barcode and the other adapter). This script
# removes those empty sequences from the fastq file.
# You need to specify the file to be processed and the starting string that 
# indicates a header line.
# usage: ./removeemptysequences.py fastqfile.fastq headerstartstring

import sys
header_start = sys.argv[2]
header_start_length = len(header_start)
empty_sequence_count = 0
good_sequence_count = 0

with open(sys.argv[1]) as file:
    fastq_line = 0
    header = ""
    data = ""
    marker = ""
    quality = ""
    is_empty_sequence = 0
    for line in file:
        if fastq_line == 1: #This is the data line
            if len(line) == 1: #empty line (just a \n character)
                is_empty_sequence = 1
            else:
                is_empty_sequence = 0
            data = line
            fastq_line = 2
        elif fastq_line == 3: # This is the quality line
            quality = line
            fastq_line = 0
        elif line[0:header_start_length] == header_start: # This is the header
            header = line
            fastq_line = 1
        elif line[0] == "+": # The quality line is next
            marker = line
            fastq_line = 3
        if fastq_line == 0: # Time to write the record if the sequence isn't empty
            if is_empty_sequence == 0: #not empty, print it
                print header, data, marker, quality,
                good_sequence_count += 1
            else:
                empty_sequence_count += 1
#print good_sequence_count, empty_sequence_count
