#! /usr/bin/python

# plotclusterreadproportions.py
# Takes a clster file from cdhit and for each cluster with more than one
# unique read, returns:
# 1) The # of unique reads
# 2) The proportion of reads that match the most common unique read
# Values are csv separated so I can scatterplot them.
# This only works if cdhit was run using the output of my renameclusters.py
# script as the input.
# usage: ./plotclusterreadproportions.py clusterfile.clstr

import sys

# Step through the clstr file
with open(sys.argv[1]) as cluster_file:
    read_count = -1
    most_common_count = 0
    total_count = 0
    unique_count = 0
    print "Proportion_of_most_common,Count_of_unique_sequences,Count_of_reads"
    for line in cluster_file:
        if line[0] == ">": # This is a new cluster. Record data for the previous cluster and start again
            if read_count != -1:
                proportion_most_common = most_common_count / float(total_count)
                if total_count >= 10: # filter out clusters with low read counts
                    print "%s,%s,%s" % (proportion_most_common, unique_count, total_count)
                most_common_count = 0
                total_count = 0
                unique_count = 0
        else:
            unique_count += 1
            read_count = int(line.split("...")[0].split(":")[-1]) # The count is between a ":" and the "..."
            total_count += read_count
            if read_count > most_common_count:
                most_common_count = read_count
    # We counted the reads for the last cluster in the file but haven't recorded it yet
    proportion_most_common = most_common_count / float(total_count)
    if total_count >= 10: # filter out clusters with low read counts
        print "%s,%s,%s" % (proportion_most_common, unique_count, total_count)
