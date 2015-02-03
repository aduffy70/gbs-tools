#! /usr/bin/python

# plotclustercounts.py
# Takes a clster file from cdhit and returns the data for a histogram
# of reads per cluster.
# This can be done with using plot_len1.pl from the cd-hit package,
# but this script is for cdhit output when my renameclusters.py
# script was used to generate the input fasta file for the cdhit run,
# i.e., you are clustering seed sequences from a previous cluster run.
# In this case, the clstr output will include the count of reads that
# were associated with each seed sequence, so we can track how many of
# the original reads are included in each newly created cluster.
# Format for specifying bin sizes is based on that of plot_len1.pl:
# ex. 1,2,3-5,6-50,51-100,101-99999
# ... this also works but with less informative bin labels in the table:
# ex. 1,2,5,50,100,99999 
# No spaces are allowed in the string, bins must be in order, must not
# overlap, and must include all possible values.
# Output is a table of sequence and cluster counts for each bin. 
# usage: ./plotclustercounts.py clusterfile.clstr binsizes

import sys

reads_total = 0
clusters_total = 0
# Parse the bin sizes
bin_strings = sys.argv[2].split(",")
bin_count = len(bin_strings)
reads_by_bin = [0] * bin_count
clusters_by_bin = [0] * bin_count
bin_max_sizes = [0] * bin_count
for x in range(0, bin_count):
    bin_max_sizes[x] = int(bin_strings[x].split("-")[-1])
# Step through the clstr file
with open(sys.argv[1]) as cluster_file:
    read_count = -1
    for line in cluster_file:
        if line[0] == ">": # This is a new cluster. Record data for the previous cluster and start again
            if read_count != -1:
                bin = 0
                while read_count > bin_max_sizes[bin]:
                    bin += 1
                clusters_by_bin[bin] += 1
                reads_by_bin[bin] += read_count
                clusters_total += 1
                reads_total += read_count
            read_count = 0
        else: # This is a cluster description
            read_count += int(line.split("...")[0].split(":")[-1]) # The count is between a ":" and the "..."
    # We counted the reads for the last cluster in the file but haven't recorded it yet
    bin = 0
    while read_count > bin_max_sizes[bin]:
        bin += 1
    clusters_by_bin[bin] += 1
    reads_by_bin[bin] += read_count
    clusters_total += 1
    reads_total += read_count
# Print the output table
print "Size\tReads\tClusters"
for bin in range(0, bin_count):
    print "%s\t%s\t%s" % (bin_strings[bin], reads_by_bin[bin], clusters_by_bin[bin])
print "Total\t%s\t%s" % (reads_total, clusters_total)
