# Read and library quality control
We removed unaligned, low quality, multi-mapped, duplicate reads and compared reads lost between our STARR-seq libraries and reanalyzed datasets (Supplemental_Fig_S2). 

We assessed data quality and replicability by calculating correlation of filtered read counts between input and output library replicates. Additionally, we calculated correlation of Reads per Million(RPM) normalized output-over-input fold changes between replicates (Supplemental_Fig_S3). The output sequencing libraries were generated from the wild-type control HEK293T line. 

To compare quality of published datasets with our data, we assessed the correlation of filtered read counts between input and output replicates for our STARR-seq libraries and the reanalyzed datasets (Johnson et al. 2018; Wang et al. 2018) (Supplemental_Fig_S4).

We also performed Principal Component Analysis (PCA) and visualized the first two principal components of input and output replicate filtered read counts for all reanalyzed datasets including our own (Supplemental_Fig_S5).

Script used to calculate reads lost after each step of deduplication, alignment and filtering pipelibe along with calculation of library wide filtered read depth is *"./src/0_get_read_qc_stats.py"*. Additionally, the script used to generate the figures described above is located in *"./notebooks/"* directory.

# Assessing reproducibility of published STARR-seq datasets
To compare variation in enhancer activity for a given fragment between different STARR-seq studies, we used processed bigwig files from Johnson and colleagues and Lee and colleagues for their respective whole genome studies (Johnson et al. 2018; Lee et al. 2020). We used output over input fold change signals from the two whole genome libraries reported by Lee and colleagues, submitted as bigwig files. Johnson and colleagues reported separate bigwig files for input and output read signals for their whole genome library. In this regard, we first normalized the input signal by Z-score normalization method. Next, we calculated fold change of output over normalized input. Finally, we measured Pearson and Spearman correlation of fold changes between the three libraries (Supplemental_Fig_S7).

Script for this analysis is present in *"./notebooks/FigS7_fc_compare_published.ipynb"*.