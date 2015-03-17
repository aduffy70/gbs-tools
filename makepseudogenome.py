#! /usr/bin/python

# makepseudogenome.py
# From a cdhit cluster of unique sequences, makes a fasta file of the 
# most common unique sequence in each cluster (since the cdhit "seeds"
# are not always the most common sequence). This can be used as a 
# pseudogenome to assemble reads against using Bowtie2 or other tools.
# usage: ./makepseudogene.py clusterfile.clstr uniquereads.fasta

import sys
import HTSeq

#Read the fastafile of unique sequences into a dictionary. This will be big (~4Gb) but should be faster than reading through the file millions of times.
unique_sequences = {}
unique_sequences_file = HTSeq.FastaReader(sys.argv[2])
for sequence in unique_sequences_file:
    unique_sequences[sequence.name] = sequence.seq
print >> sys.stderr, "Indexed unique sequences"
#Step through the cluster file
with open(sys.argv[1]) as cluster_file:
    cluster_name = ""
    most_common_count = 0
    most_common_name = ""
    total_reads = 0
    for line in cluster_file:
        if line[0] == ">": #This is a new cluster, write the data for the last cluster
            if cluster_name != "": #Print the last cluster info
                if total_reads > 1: #Don't bother writing singletons to the pseudogenome
                    print cluster_name
                    print unique_sequences[most_common_name]
            cluster_name = line.strip().replace(" ", "_")
            most_common_count = 0
            total_reads = 0        
        else: #this is a unique sequence. See if it is most common so far
            count = int(line.split("...")[0].split(":")[-1]) # the count is between : and ...
            if count > most_common_count:
                most_common_count = count
                most_common_name = line.split("...")[0].split(">")[-1] # name is between > and ...
            total_reads += most_common_count
#when we finish reading the file we still haven't printed the info for the last cluster, so do it now
if total_reads > 1:
    print cluster_name
    print unique_sequences[most_common_name]

