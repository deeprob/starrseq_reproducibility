# In-house STARR-Seq dataset description and usage
Our persective on reproducibility of STARR-Seq assays uses in-house generated dataset. We used our data to demonstrate the effects of read filtering, significance of read depth, and compared different peak callers. All sequence data generated in this study have been submitted to the NCBI BioProject database (https://www.ncbi.nlm.nih.gov/bioproject/) under accession number PRJNA879724. 

We built a STARR-seq plasmid library spanning approximately 33 Mbp of the human genome and performed multiple STARR-seq runs on HEK293T cells. Our target regions were shortlisted from existing ChIP-seq data on HEK293 or HEK293T cells available on ENCODE (Birney et al. 492007). In brief, we first overlapped ChIP-seq sites binding to the histone modifications H3K27Ac (for active enhancers) and H3K4Me1 (for active or poised enhancers). Next, we intersected these regions with all TF-ChIP-seq sites on HEK293 (from ENCODE) to obtain a comprehensive enhancer catalog spanning 46,142 ChIP-seq sites. The selected regions comprise TF-binding sites that overlap with recognized enhancer marks and their chromosomal coordinates are given in the file *master.bed*. 

We captured our target library from commercially available human whole genome DNAusing hybridization and capture probes and cloned the captured fragments into the human STARR-seq vector to build a STARR-seq plasmid library (see Supplemental_Fig_S1, STARR-seq Protocol). To assess the impact of different genomic mutations on enhancer activity, we transfected the library into seven different mutant HEK293T lines and one wild-type line in three biological replicates and isolated reporter specific mRNA to build 24 STARR-seq output screening libraries. We directly amplified the STARR-seq plasmid library in three replicates for the input. We sequenced 24 output screening libraries and 3 input libraries using a NextSeq2000 sequencer with approximately 45 million reads per sample.

# STARR-seq library region selection

To construct STARR-seq libraries, potential enhancer regions were selected based on chromatin signatures and TF binding sites.

**PS. This was originally prepared by Matt.**

# STEPS

1. Union of H3K4me1 and H3K27ac sites

2. Removal of 2kb TSS sites

3. Keep histones sites that intersect with at least 1 TF ChIP site in Hek cells or EP300 ChIP site in other cell lines

4. Pad less than 500 bp regions

# Output

Master file with a list of potential enhancer regions 

# Script descriptions

1. root/src/0_download_encode_data.py: Downloads Chip-Seq data of histones, TFs and p300 from encode in hek293/hela/k562 cell lines.
2. root/src/1_liftover_tcf7l2.py: TCF7L2 chip seq data was aligned to hg19 genome assembly. This script does liftover to hg38.
3. root/src/2_get_tss.py: Gets the genomic coordinates of TSSs of refseq genes.
4. root/src/3_create_master+list.py: This script follows the above steps and generates a list of regions to conduct STARRSeq on.
