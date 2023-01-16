# manually rename files according to the starrseq computational analysis convention
import os
import logging


FILENAME_MAP_DICT = {
    "SRR7122187_1.fastq": "A549_12_output_B1_R1.fastq",
    "SRR7122187_2.fastq": "A549_12_output_B1_R2.fastq", 
    "SRR7122188_1.fastq": "A549_12_output_B2_R1.fastq",
    "SRR7122188_2.fastq": "A549_12_output_B2_R2.fastq",
    "SRR7122189_1.fastq": "A549_12_output_B3_R1.fastq",
    "SRR7122189_2.fastq": "A549_12_output_B3_R2.fastq", 
    "SRR7122190_1.fastq": "A549_12_output_B4_R1.fastq",
    "SRR7122190_2.fastq": "A549_12_output_B4_R2.fastq",
    "SRR7122191_1.fastq": "A549_12_output_B5_R1.fastq",
    "SRR7122191_2.fastq": "A549_12_output_B5_R2.fastq",
    "SRR7122192_1.fastq": "A549_input_B1_R1.fastq",
    "SRR7122192_2.fastq": "A549_input_B1_R2.fastq",
    "SRR7122193_1.fastq": "A549_input_B2_R1.fastq",
    "SRR7122193_2.fastq": "A549_input_B2_R2.fastq",
    "SRR7122194_1.fastq": "A549_input_B3_R1.fastq",
    "SRR7122194_2.fastq": "A549_input_B3_R2.fastq",
    "SRR7122195_1.fastq": "A549_input_B4_R1.fastq",
    "SRR7122195_2.fastq": "A549_input_B4_R2.fastq",
    "SRR7122196_1.fastq": "A549_input_B5_R1.fastq",
    "SRR7122196_2.fastq": "A549_input_B5_R2.fastq",
    "SRR7122197_1.fastq": "A549_input_B6_R1.fastq",
    "SRR7122197_2.fastq": "A549_input_B6_R2.fastq",
    "SRR7122198_1.fastq": "A549_input_B7_R1.fastq",
    "SRR7122198_2.fastq": "A549_input_B7_R2.fastq",
    "SRR7122199_1.fastq": "A549_input_B8_R1.fastq",
    "SRR7122199_2.fastq": "A549_input_B8_R2.fastq",
    "SRR7122200_1.fastq": "A549_input_B9_R1.fastq",
    "SRR7122200_2.fastq": "A549_input_B9_R2.fastq",
    "SRR7122201_1.fastq": "A549_input_B10_R1.fastq",
    "SRR7122201_2.fastq": "A549_input_B10_R2.fastq",
    "SRR7122202_1.fastq": "A549_input_B11_R1.fastq",
    "SRR7122202_2.fastq": "A549_input_B11_R2.fastq",
    "SRR7122203_1.fastq": "A549_input_B12_R1.fastq",
    "SRR7122203_2.fastq": "A549_input_B12_R2.fastq",
}


def rename_file(filename):
    if filename in FILENAME_MAP_DICT.keys():
        newname = FILENAME_MAP_DICT[filename]
        logging.info(f"Renaming {filename} to {newname}!")
        os.rename(filename, newname)
    return


if __name__ == "__main__":
    renaming_dir = "/data5/deepro/starrseq/main_library/1_dedup_align_filter/data/others/johnson_reddy/raw_data"
    logging.basicConfig(filename=os.path.join(renaming_dir, "file_rename.log"), encoding='utf-8', level=logging.INFO)
    for file in os.scandir(renaming_dir):
        rename_file(file.name)
