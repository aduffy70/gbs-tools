#! /usr/bin/python

# findunique12mers.py
# In my GBS fastq file, what unique 12mer starting sequences exist not
# including those with Ns?  
# Actually an N can be handled just like any other mismatched base so
# lets do this again with them included.
# You need to specify the starting string that indicates a header line
# and the length of the longest barcode/stickyend combination.
# usage: ./findunique12mers.py fastqfile.fastq headerstartstring maxbarcodelength

import sys

header_line = 0
sequence_count = 0
n_count = 0
clean_count = 0
unique_starts = {}
header_start = sys.argv[2]
header_start_length = len(header_start)
max_barcode_length = int(sys.argv[3])

with open(sys.argv[1]) as file:
    for line in file:
        if header_line == 1: #This is the data line
            target = line[0:max_barcode_length]
# Use this section to exclude 12mers containing Ns            
#            if "N" in target:
#                n_count += 1
#            else:
#                clean_count += 1
#                if unique_starts.has_key(target):
#                    unique_starts[target] += 1
#                else:
#                    unique_starts[target] = 1
# end section

# Use this section to include 12mers with Ns
            if target in unique_starts:
                unique_starts[target] += 1
            else:
                unique_starts[target] = 1
# end section

            sequence_count += 1
            header_line = 0
        elif line[0:header_start_length] == header_start: #This is the header, the dataline is next
            header_line = 1
print "# Total reads:", sequence_count
#print "# Reads with N's:", n_count
#print "# Reads without N's", clean_count
print "# Unique 12mers:", len(unique_starts)
print "# Reads beginning with each unique 'barcode':"
for key in unique_starts:
    print key, unique_starts[key]
