#! /usr/bin/python

# pairwise_coverage.py
# Do pairwise comparisons of samples to see which samples share the most loci.
# Obviously, two samples with lots of loci have the potential to share more
# than two samples with few loci or one with many and one with few, so report
# it as a percentage of the loci of the smallest of each pair. For each sample
# we would still expect that percentage to decrease in comparisons with samples
# with fewer loci, but we are just looking for gross outliers from the pattern
# which may suggest misidentified species mixed into the sample set.
# Uses a genotype_table file (such as All_GTs.txt from npGeno) and a list of 
# the sample names in the order that they should appear in the output table 
# (sorting by # of loci, reads, or ratio of reads:loci all seem useful) - one 
# locus name per line and the locus names must match the names in the header 
# of the genotypes table.
# Usage: pairwise_coverage.py genotype_table_file.txt sorted_samples.txt

import sys

#Make a list of sample names in the order we want to display them in the output
with open(sys.argv[2]) as sample_file:
    sample_order = []
    for sample in sample_file:
        sample_order.append(sample.strip())
    sample_count = len(sample_order)

#Build a list of lists to hold our comparison table
comp_table = []
for row in range(0,sample_count):
    cols = [0] * sample_count
    comp_table.append(cols)

#Make a list to hold the count of loci per sample (by sample_order)
locus_counts_by_sample = [0] * sample_count
    
with open(sys.argv[1]) as gt_file: # open the genotypes table file
    is_header = True
    header_order = []    
    for locus in gt_file:
        if is_header: #Grab the sample name info from the header so we know what order the samples are in on the table
            elements = locus.strip().split()[2:] #skip the locus and ref
            for sample_name in elements: 
                header_order.append(sample_name)
            #Build a header_order to sample_order lookup table (we will know the header_order and want to know the sample_order
            hs_lookup = []
            for sample in header_order:
                hs_lookup.append(sample_order.index(sample))
            is_header = False
        else: #process the locus and update the comparison table
            elements = locus.strip().split()[3:] #skip the locus (first two columns) and ref
            for y in range(0, sample_count):
                if elements[y] != 'NA':
                    locus_counts_by_sample[hs_lookup[y]] += 1
                    for x in range(y, sample_count):
                        if elements[x] != 'NA': #present in both samples
                            comp_table[hs_lookup[y]][hs_lookup[x]] += 1
                            if x != y:
                                comp_table[hs_lookup[x]][hs_lookup[y]] += 1 #we have to fill on both halves of the table (x,y and y,x) because we are re-ordering things so we can't be certain all values will be in the top half of the re-ordered table, but we don't want to fill the diagonal (y=x) cells twice

#Ouput the locus counts by sample - we can verify this against the log output from when we made the genotypes table
print "Locus_counts_by_sample:"
for sample_name in sample_order:
    print sample_name,
print ''
for locus_count in locus_counts_by_sample:
    print locus_count,
print '\n'

#Output the comparison table but convert the values to a percentage of the smaller of the two samples being compared
print "Pairwise % shared loci\n   ",
for sample_name in sample_order:
    print sample_name,
print''
for y in range(0,sample_count):
    print sample_order[y],
    for x in range(0, sample_count):
        if x==y:
            print "---",  # don't print the self-comparisons. All those 100%s it aren't informative and make heatmaps harder to interpret
        else:
            lesser = min(locus_counts_by_sample[y], locus_counts_by_sample[x]) 
            loci_percent = comp_table[y][x] / float(lesser) * 100
            print "%3d" % loci_percent,
    print ''
