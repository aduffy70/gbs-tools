#! /usr/bin/python

# renameclusterseeds.py
# Takes the fasta output from cd-hit-454 and replaces the name of each
# representative "seed" sequence with the name of the cluster from the 
# clster output file. This way I can recluster this output at 
# different stringencies and the output of those clustering runs will 
# directly report which cluster numbers were combined. 
# Renames the reads using a tag to identify the clustering run and the
# cluster number, and number of reads in the cluster separated by colons. 
# Example: >cintricatum_1.0:cluster_2:87
# usage: ./renameclusterseeds.py fastafile.fasta clusterfile.clstr tag

import sys
import HTSeq
# Step through the fasta file, modify the description and output the record
fasta_file = HTSeq.FastaReader(sys.argv[1])
fasta_reads = iter(fasta_file) # create an iterable so we can step through it with next()
tag = sys.argv[3]
script_failed = 0 # If the cluster file and fasta file aren't in the same order, this won't work 
with open(sys.argv[2]) as cluster_file:
    cluster_number = ""
    read_count = 0
    for line in cluster_file:
        if line[0] == ">": # This is a new cluster. Print the last cluster and start again
            if cluster_number != "": # Print the last cluster info
                if script_failed == 1:
                    print "Seed sequence and cluster order do not match!"
                else:        
                    new_name = "%s:%s:%s" % (tag, cluster_number, read_count)
                    fasta_read.name = new_name
                    fasta_read.descr = "" # Should be already, but just in case...
                    fasta_read.write_to_fasta_file(sys.stdout)
            cluster_number = line[1:].strip() # Grab the name without the > or \n characters
            cluster_number = cluster_number.replace(" ","_") # Replace the space between "Cluster" and the number with an "_"
        elif line[0] == "0": # This is the seed for the cluster
            # it looks something like this:
            # 0   87nt, >Some_fasta_description... *
            # and we want to make sure the fasta description matches the description of the next read in the fasta file
            # if it doesn't this script won't work, but they SHOULD be in the same order
            cluster_name = line.split(">")[1].split("...")[0]
            fasta_read = fasta_reads.next()
            if fasta_read.name != cluster_name:
                # script failed
                script_failed = 1
            read_count = 1
        else:
            read_count += 1
