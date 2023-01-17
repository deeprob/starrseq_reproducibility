# Challenges and considerations for reproducibility of STARR-seq assays
Codebase for manuscript titled "Challenges and considerations for reproducibility of STARR-seq assays" by Maitreya Das, Ayaan Hossain, Deepro Banerjee, Craig Alan Praul, Santhosh Girirajan; bioRxiv 2022.07.27.501795; doi: https://doi.org/10.1101/2022.07.27.501795

# Repository guidelines
This repo contains step-by-step guide to the analysis carried out for "Challenges and considerations for reproducibility of STARR-seq assays". A description of each sub dir is as follows:

1. **0_in-house_dataset**: Details about in-house STARR-seq library generation along with selection of potential enhancer regions required to construct the library is present here.

2. **1_data_download**: Instructions about downloading and organizing raw data of the in-house STARR-seq library and other published datasets analyzed as part of the manuscript is present here.

3. **2_dedup_align_filter**: Links to our custom made deduplication, alignment and filtering pipeline of raw STARR-seq reads along with bash scripts used to run the pipeline is present here.

4. **3_read_lib_qc**: Read and Library quality control analysis scripts of deduped, aligned and filtered STARR-seq reads is present here.

5. **4_peak_call**: Links to the STARR-seq peak calling pipeline along with bash scripts used to run the pipeline is present here.

6. **5_peak_qc**: Quality control analysis scripts of STARR-seq peaks is present here.
