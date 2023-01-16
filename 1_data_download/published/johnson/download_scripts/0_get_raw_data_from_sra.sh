#!/bin/bash

echo `date` starting job on $HOSTNAME

# download sra accession from the project page link: https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP144640&o=acc_s%3Aa
# manually remove accession numbers which are not relevant - only keep input and 12hrs dex treated SRA runs
# /data5/deepro/sw/edirect/edirect/esearch -db sra -query SRP144640 | /data5/deepro/sw/edirect/edirect/efetch -format runinfo | cut -d ',' -f 1 | grep SRR > SRR_Acc_List.txt

# prefetch files
/data5/deepro/sw/sra/sratoolkit.3.0.0-ubuntu64/bin/prefetch --option-file ./SRR_Acc_List.txt

# manually edit the accession list to select only required datsets

# download fastq files for SRR data
cat ./SRR_Acc_List.txt | xargs -I {} /data5/deepro/sw/sra/sratoolkit.3.0.0-ubuntu64/bin/fasterq-dump --split-files -t /data5/deepro/tmp {}/{}.sra

echo `date` ending job
