gbs-tools
=========

Tools for processing genotyping-by-sequencing data 

checkfastqformat.py - Checks a fastq file for formatting issues. 
findNs.py - Reports on Ns in the first 12 nucleotides of reads in a fastq file. 
exploreabmiguous.py - For 12mers that are equally distant to more than one 
                      barcode/stickyend with a distance of 1 or 2, return the 
                      12mer, the distance, and the list of equally distant barcodes. 
findbarcode.py - Searches for a specific barcode anywhere within the reads of a fastq file.
makerandom12mers.py - Generates a dummy fasta file of random 12bp sequences. Useful for
                      checking whether my pipeline is returning better results than are
                      expected just by chance in a large dataset.
