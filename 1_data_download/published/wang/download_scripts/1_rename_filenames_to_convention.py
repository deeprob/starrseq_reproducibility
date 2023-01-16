# manually rename files according to the starrseq computational analysis convention
import os
import logging


FILENAME_MAP_DICT = {
    "SRR6050484_1.fastq.gz": "GM12878_input_B1_T1_R1.fastq.gz",
    "SRR6050484_2.fastq.gz": "GM12878_input_B1_T1_R2.fastq.gz", 
    "SRR6050485_1.fastq.gz": "GM12878_input_B1_T2_R1.fastq.gz",
    "SRR6050485_2.fastq.gz": "GM12878_input_B1_T2_R2.fastq.gz",
    "SRR6050486_1.fastq.gz": "GM12878_input_B1_T3_R1.fastq.gz",
    "SRR6050486_2.fastq.gz": "GM12878_input_B1_T3_R2.fastq.gz",
    "SRR6050487_1.fastq.gz": "GM12878_input_B1_T4_R1.fastq.gz",
    "SRR6050487_2.fastq.gz": "GM12878_input_B1_T4_R2.fastq.gz",
    "SRR6050488_1.fastq.gz": "GM12878_input_B2_T1_R1.fastq.gz",
    "SRR6050488_2.fastq.gz": "GM12878_input_B2_T1_R2.fastq.gz",
    "SRR6050489_1.fastq.gz": "GM12878_input_B2_T2_R1.fastq.gz",
    "SRR6050489_2.fastq.gz": "GM12878_input_B2_T2_R2.fastq.gz",
    "SRR6050490_1.fastq.gz": "GM12878_input_B2_T3_R1.fastq.gz",
    "SRR6050490_2.fastq.gz": "GM12878_input_B2_T3_R2.fastq.gz",
    "SRR6050491_1.fastq.gz": "GM12878_input_B2_T4_R1.fastq.gz",
    "SRR6050491_2.fastq.gz": "GM12878_input_B2_T4_R2.fastq.gz",
    "SRR6050492_1.fastq.gz": "GM12878_input_B3_T1_R1.fastq.gz",
    "SRR6050492_2.fastq.gz": "GM12878_input_B3_T1_R2.fastq.gz",
    "SRR6050493_1.fastq.gz": "GM12878_input_B3_T2_R1.fastq.gz",
    "SRR6050493_2.fastq.gz": "GM12878_input_B3_T2_R2.fastq.gz",
    "SRR6050494_1.fastq.gz": "GM12878_input_B3_T3_R1.fastq.gz",
    "SRR6050494_2.fastq.gz": "GM12878_input_B3_T3_R2.fastq.gz",
    "SRR6050495_1.fastq.gz": "GM12878_input_B3_T4_R1.fastq.gz",
    "SRR6050495_2.fastq.gz": "GM12878_input_B3_T4_R2.fastq.gz",
    "SRR6050496_1.fastq.gz": "GM12878_input_B4_T1_R1.fastq.gz",
    "SRR6050496_2.fastq.gz": "GM12878_input_B4_T1_R2.fastq.gz",
    "SRR6050497_1.fastq.gz": "GM12878_input_B4_T2_R1.fastq.gz",
    "SRR6050497_2.fastq.gz": "GM12878_input_B4_T2_R2.fastq.gz",
    "SRR6050498_1.fastq.gz": "GM12878_input_B4_T3_R1.fastq.gz",
    "SRR6050498_2.fastq.gz": "GM12878_input_B4_T3_R2.fastq.gz",
    "SRR6050499_1.fastq.gz": "GM12878_input_B4_T4_R1.fastq.gz",
    "SRR6050499_2.fastq.gz": "GM12878_input_B4_T4_R2.fastq.gz",
    "SRR6050500_1.fastq.gz": "GM12878_input_B5_T1_R1.fastq.gz",
    "SRR6050500_2.fastq.gz": "GM12878_input_B5_T1_R2.fastq.gz",
    "SRR6050501_1.fastq.gz": "GM12878_input_B5_T2_R1.fastq.gz",
    "SRR6050501_2.fastq.gz": "GM12878_input_B5_T2_R2.fastq.gz",
    "SRR6050502_1.fastq.gz": "GM12878_input_B5_T3_R1.fastq.gz",
    "SRR6050502_2.fastq.gz": "GM12878_input_B5_T3_R2.fastq.gz",
    "SRR6050503_1.fastq.gz": "GM12878_input_B5_T4_R1.fastq.gz",
    "SRR6050503_2.fastq.gz": "GM12878_input_B5_T4_R2.fastq.gz",
    "SRR6050504_1.fastq.gz": "GM12878_output_B1_T1_R1.fastq.gz",
    "SRR6050504_2.fastq.gz": "GM12878_output_B1_T1_R2.fastq.gz",
    "SRR6050505_1.fastq.gz": "GM12878_output_B1_T2_R1.fastq.gz",
    "SRR6050505_2.fastq.gz": "GM12878_output_B1_T2_R2.fastq.gz",
    "SRR6050506_1.fastq.gz": "GM12878_output_B1_T3_R1.fastq.gz",
    "SRR6050506_2.fastq.gz": "GM12878_output_B1_T3_R2.fastq.gz",
    "SRR6050507_1.fastq.gz": "GM12878_output_B1_T4_R1.fastq.gz",
    "SRR6050507_2.fastq.gz": "GM12878_output_B1_T4_R2.fastq.gz",
    "SRR6050508_1.fastq.gz": "GM12878_output_B2_T1_R1.fastq.gz",
    "SRR6050508_2.fastq.gz": "GM12878_output_B2_T1_R2.fastq.gz",
    "SRR6050509_1.fastq.gz": "GM12878_output_B2_T2_R1.fastq.gz",
    "SRR6050509_2.fastq.gz": "GM12878_output_B2_T2_R2.fastq.gz",
    "SRR6050510_1.fastq.gz": "GM12878_output_B2_T3_R1.fastq.gz",
    "SRR6050510_2.fastq.gz": "GM12878_output_B2_T3_R2.fastq.gz",
    "SRR6050511_1.fastq.gz": "GM12878_output_B2_T4_R1.fastq.gz",
    "SRR6050511_2.fastq.gz": "GM12878_output_B2_T4_R2.fastq.gz",
    "SRR6050512_1.fastq.gz": "GM12878_output_B3_T1_R1.fastq.gz",
    "SRR6050512_2.fastq.gz": "GM12878_output_B3_T1_R2.fastq.gz",
    "SRR6050513_1.fastq.gz": "GM12878_output_B3_T2_R1.fastq.gz",
    "SRR6050513_2.fastq.gz": "GM12878_output_B3_T2_R2.fastq.gz",
    "SRR6050514_1.fastq.gz": "GM12878_output_B3_T3_R1.fastq.gz",
    "SRR6050514_2.fastq.gz": "GM12878_output_B3_T3_R2.fastq.gz",
    "SRR6050515_1.fastq.gz": "GM12878_output_B3_T4_R1.fastq.gz",
    "SRR6050515_2.fastq.gz": "GM12878_output_B3_T4_R2.fastq.gz",
    "SRR6050516_1.fastq.gz": "GM12878_output_B4_T1_R1.fastq.gz",
    "SRR6050516_2.fastq.gz": "GM12878_output_B4_T1_R2.fastq.gz",
    "SRR6050517_1.fastq.gz": "GM12878_output_B4_T2_R1.fastq.gz",
    "SRR6050517_2.fastq.gz": "GM12878_output_B4_T2_R2.fastq.gz",
    "SRR6050518_1.fastq.gz": "GM12878_output_B4_T3_R1.fastq.gz",
    "SRR6050518_2.fastq.gz": "GM12878_output_B4_T3_R2.fastq.gz",
    "SRR6050519_1.fastq.gz": "GM12878_output_B4_T4_R1.fastq.gz",
    "SRR6050519_2.fastq.gz": "GM12878_output_B4_T4_R2.fastq.gz",
    "SRR6050520_1.fastq.gz": "GM12878_output_B5_T1_R1.fastq.gz",
    "SRR6050520_2.fastq.gz": "GM12878_output_B5_T1_R2.fastq.gz",
    "SRR6050521_1.fastq.gz": "GM12878_output_B5_T2_R1.fastq.gz",
    "SRR6050521_2.fastq.gz": "GM12878_output_B5_T2_R2.fastq.gz",
    "SRR6050522_1.fastq.gz": "GM12878_output_B5_T3_R1.fastq.gz",
    "SRR6050522_2.fastq.gz": "GM12878_output_B5_T3_R2.fastq.gz",
    "SRR6050523_1.fastq.gz": "GM12878_output_B5_T4_R1.fastq.gz",
    "SRR6050523_2.fastq.gz": "GM12878_output_B5_T4_R2.fastq.gz",
    "SRR6050524_1.fastq.gz": "GM12878_inputlong_B1_T1_R1.fastq.gz",
    "SRR6050524_2.fastq.gz": "GM12878_inputlong_B1_T1_R2.fastq.gz",
    "SRR6050524_3.fastq.gz": "GM12878_inputlong_B1_T1_R3.fastq.gz",
    "SRR6050525_1.fastq.gz": "GM12878_inputlong_B1_T2_R1.fastq.gz",
    "SRR6050525_2.fastq.gz": "GM12878_inputlong_B1_T2_R2.fastq.gz",
    "SRR6050525_3.fastq.gz": "GM12878_inputlong_B1_T2_R3.fastq.gz",
    "SRR6050526_1.fastq.gz": "GM12878_inputlong_B1_T3_R1.fastq.gz",
    "SRR6050526_2.fastq.gz": "GM12878_inputlong_B1_T3_R2.fastq.gz",
    "SRR6050526_3.fastq.gz": "GM12878_inputlong_B1_T3_R3.fastq.gz",
    "SRR6050527_1.fastq.gz": "GM12878_inputlong_B1_T4_R1.fastq.gz",
    "SRR6050527_2.fastq.gz": "GM12878_inputlong_B1_T4_R2.fastq.gz",
    "SRR6050527_3.fastq.gz": "GM12878_inputlong_B1_T4_R3.fastq.gz",

}


def rename_file(filename):
    if filename in FILENAME_MAP_DICT.keys():
        newname = FILENAME_MAP_DICT[filename]
        logging.info(f"Renaming {filename} to {newname}!")
        os.rename(filename, newname)
    return


if __name__ == "__main__":
    renaming_dir = "/data5/deepro/starrseq/main_library/1_dedup_align_filter/data/others/wang_kellis/raw_data"
    logging.basicConfig(filename=os.path.join(renaming_dir, "file_rename.log"), encoding='utf-8', level=logging.INFO)
    for file in os.scandir(renaming_dir):
        rename_file(file.name)
