#! /usr/bin/python

# movefastabarcode.py
# Moves the sample name and barcode from the end of the fasta description
# to the start. Just keep the info needed to tie back to the read in the 
# original fastq file - dump everything that is the same on each read.
# In the cluster output from cd-hit-454, it only includes the fasta 
# description up to the first space, which was cutting off the
# sample name and barcode, while saving all the not-so-useful info about
# which machine, lane, etc the read is from. 
# usage: ./movefastabarcode.py fastafile.fasta

import sys
import HTSeq
# Step through the fasta file, modify the description and output the record
fasta_file = HTSeq.FastaReader(sys.argv[1])
for read in fasta_file:
    name = read.name.split(":")
    descr = read.descr.split(":")
    # HTSeq splits the fasta description line at the first space and calls everything before the name and everything after the descr
    # name elements:
    #   0-3 machine, run, lane (discard)
    #   4-6 location of the read on the flowcell combine to uniquely identify the read (keep)
    # descr elements  
    #   -1 barcode (keep)
    #   -2 sample name (keep)
    #   -3 restriction cutsite (discard)
    #   everything else (discard)
    read.name = "%s:%s:%s:%s:%s" % (descr[-2], descr[-1], name[4], name[5], name[6])
    read.descr = ""
    read.write_to_fasta_file(sys.stdout)

