# Read deduplication, alignment,and filtering
We used a custom-made computational pipeline to analyze raw fastq files from STARR-seq input and output libraries. Our deduplication-alignment-filtering pipeline is posted here: https://github.com/deeprob/starrseq_dedup_align_filter. 

Pipeline input: STARR-Seq input/output library raw fastq read pairs and umi file (if available).
Pipeline output: STARR-Seq input/output library bam files aligned to an user specified genome. 
