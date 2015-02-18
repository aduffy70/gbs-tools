#! /usr/bin/python

# findunique12mers.py
# In a GBS fastq file, what unique starting sequences (barcodes
# plus RE sticky ends) exist and how many times is each found?  
# You need to specify the the length of the longest barcode plus
# sticky end.
# usage: ./findunique12mers.py fastqfile.fastq maxbarcodelength

import sys
import HTSeq

unique_starts = {}
max_barcode_length = int(sys.argv[2])
sequence_count = 0

fastq_file = HTSeq.FastqReader(sys.argv[1])
for read in fastq_file:
    target = read.seq[0:max_barcode_length]
    if target in unique_starts:
        unique_starts[target] += 1
    else:
        unique_starts[target] = 1
    sequence_count += 1
print "# Total reads:", sequence_count
print "# Unique starting sequences:", len(unique_starts)
print "# Unique_starting_sequence Read_count"
for key in unique_starts:
    print key, unique_starts[key]
