# Peak calling
We called peaks using previously published tools, MACS2(Zhang et al. 2008), STARRPeaker (Lee et al. 2020), CRADLE (Kim et al. 2021)and DESeq2 (Love et al. 2014) using default settings. Our peak calling pipeline is posted on GitHub: https://github.com/deeprob/starrseq_peak_call.

**Pipeline input**: Reference genome aligned STARR-Seq input/output library bam files along with tool specific files for CRADLE and STARRPeaker.

**Pipeline output**: Chromosomal coordinates with higher than expected output over input fold changes or peaks. 
