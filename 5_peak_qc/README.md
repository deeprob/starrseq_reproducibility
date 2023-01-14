# Variation in number of peaks called with coverage
For comparing the number of peaks by varying library coverage, we randomly subsampled the input and output control libraries from 10% to 90% with increments of 5% using SAMtools (Li et al. 2009). For each subsample, we also created three replicates by changing random seed parameter. We called peaks in the subsampled libraries using STARRPeaker with the default settings (Fig 3D).

# Activity comparison between peaks and exonic regions
To compare activity between peaks and exonic regions, we first identified regions in our library which overlapped with known exonic regions from the reference human genome(GRCh38). Next, we calculated the RPKM normalized coverage of filtered reads fold changes between output and input libraries for both STARRPeaker called peaks and the identified exonic regions. Finally, we compared the fold change distributions between peaks and exonic regions using t-test (Supplemental_Fig_S6).
