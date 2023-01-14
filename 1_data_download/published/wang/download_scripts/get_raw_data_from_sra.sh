#!/bin/bash

echo `date` starting job on $HOSTNAME

# download sra accession from the project page link: https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP118092&o=acc_s%3Aa
/data5/deepro/sw/edirect/edirect/esearch -db sra -query SRP118092 | /data5/deepro/sw/edirect/edirect/efetch -format runinfo | cut -d ',' -f 1 | grep SRR > SRR_Acc_List.txt

# manually edit the accession list ot select only required datsets

# download fastq files for SRR data
cat ./SRR_Acc_List.txt | xargs -n 1 -P 2 /data5/deepro/sw/sra/sratoolkit.3.0.0-ubuntu64/bin/fastq-dump --split-files --gzip

echo `date` ending job
