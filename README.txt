gbs-tools
=========

Tools for processing genotyping-by-sequencing data 

checkfastqformat.py - Checks a fastq file for formatting issues. 
findNs.py - Reports on Ns in the first 12 nucleotides of reads in a fastq file. 
exploreabmiguous.py - For 12mers that are equally distant to more than one 
                      barcode/stickyend with a distance of 1 or 2, return the 
                      12mer, the distance, and the list of equally distant 
                      barcodes. 
findbarcode.py - Searches for a specific barcode anywhere within the reads of 
                 a fastq file.
makerandom12mers.py - Generates a dummy fasta file of random 12bp sequences.
                      Useful for checking whether my pipeline is returning 
                      better results than are expected just by chance in a 
                      large dataset.
collapsebarcodes.py - Removes a single nucleotide from the end of a set of 
                      12mer (or whatever-mer) sequences to see how the list 
                      of unique sequences collapses. Didn't end up being useful.
countsbysample.py - Returns a count of how many reads in a fastq file were 
                    assigned to each barcode.
compare12merquality.py - Compares 12mers to the closest matching barcode and 
                         reports the average quality of matching vs mismatched
                         bases.
compare12merquality-zd.py - Same, but for data with 14-16mers instead of 12mers.
categorizemismatch.py - Compares 12mers to the closest matching barcode and
                        categorizes the mismatches by type (A to C, C to G,
                        etc).
justthedata.py - Pulls out just the data line from a fastq file to make a    
                 smaller, more manageable file for scripts that don't need the
                 header or quality lines
doublecheckdups.py - Double check that a list of unique starting sequences is 
                     really unique.
removeemptysequences.py - Returns just records with non-zero length sequences 
                          from a fastq file.
getbarcodecounts.py - Counts how many reads and bases are assigned to each
                      barcode in a fastq file.
splitfastq.py - Splits a fastq file into mutiple files based on a list of
                barcodes and which file they belong in.

"Pipeline" used to clean up T. intricatum GBS dataset (This process could
 sped up drastically if some of these scripts were combined, but I left the
 steps in separate scripts for flexibility):

1) Make a list of unique starting sequences (potential barcode-stickyends)
   found in the fastq file. (It says 12mers, but the length is configurable.)
      findunique12mers.py
2) For each unique starting sequence, determine which of our 
   barcode-stickyends is the nearest match and the distance.
      sortbarcodes-wobble.py - for data with "wobble" bases in the cutsite 
                               (R, W, etc.)
      sortbarcodes-indels.py - if you don't have wobble bases and want to 
                               allow for indels when calculating distances
3) Where the nearest match is unambiguous and the distance is < a specified
   value, replace the starting characters of each read in the fastq data 
   with the corrected barcode-stickyend. Sort reads with ambiguous matches
   or larger distances into files to be explored separately.
      correctbarcodes.py
4) Trim the barcode-stickyends from the reads and store the sticky end, sample
   name, and barcode in the fastq description line. Trim the fastq quality 
   line to match.
      trimbarcodes.py
5) Trim any Illumina primer sequence from the 3' end of the reads and trim the
   quality line to match.
      Used "cutadapt"
6) Remove any 0-length sequences from the fastq file (with the right cutadapt
   options this might not be necessary) because they cause problems for some 
   of the fastx tools.
      removeemptysequences.py
7) Get a baseline for sequence quality before quality trimming.
      Used "fastx_quality_stats"
8) Trim trailing low quality bases.
      Used "fastq_quality_trimmer"
9) Check quality after trimming and compare to baseline.
      Used "fastx_quality_stats"
10) Split C. intricatum, T. boschiana, and D. petersii reads into three
    separate files.
      splitfastq.py
11) Sort C.intricatum file by decreasing read length
      Used "sort.pl"

