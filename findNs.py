#! /usr/bin/python

# findNs.py
# In my GBS fastq file, how many sequences have N's in the barcode/stickyend
# and where?
# Checks the first 12 nucleotides of each read in a fastq file for Ns. 
# Reports:
#   the total number of reads,
#   the number of reads with each unique pattern of Ns,
#   the number of reads with each count of Ns (0-12)
#   the number of reads with an N at each position in the sequence (1-12)
# Usage: findNs.py fastqfile.fastq

import sys

header_line = 0
sequence_count = 0
n_patterns = {} # dictionary of patterns of N's within the 1st 12 bases
n_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0] # count of reads with 0N's, 1N, 2N's...
n_positions = [0,0,0,0,0,0,0,0,0,0,0,0] # count of N's at each of the 12 bases

with open(sys.argv[1]) as file:
    for line in file:
        if header_line == 1: #This is the data line
            target = line[0:12]
            pattern = ""
            count = 0
            for base in range(0,12):
                if target[base] == "N":
                    pattern += "N"
                    count += 1
                    n_positions[base] += 1
                else:
                    pattern += "_"
            if n_patterns.has_key(pattern):
                n_patterns[pattern] += 1
            else: 
                n_patterns[pattern] = 1
            n_counts[count] += 1
            sequence_count += 1
            header_line = 0
        elif line[0:6] == "@HISEQ": #This is the header, the dataline is next
            header_line = 1
print "Total reads:", sequence_count
print "\nNumber of reads with each pattern of N's:"
for key in n_patterns:
    print key, n_patterns[key]
print "\nNumber of reads with x N's:"
for x in range(0,13):
    print x, n_counts[x]
print "\nTotal number of N's at each base position:"
for x in range(0,12):
    print x+1, n_positions[x]
