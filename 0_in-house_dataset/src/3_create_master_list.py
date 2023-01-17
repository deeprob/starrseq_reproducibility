import os
import pandas as pd
import pybedtools
import numpy as np


h3k4me1_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/hek293/chip/matt_downloaded_histones/HEK293_H3K4me1_hg38.bed"
h3k27ac_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/hek293/chip/matt_downloaded_histones/HEK293_H3K27ac_hg38.bed"
tss_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/tss/refseq_gene_tss_2kb.bed"
tf_dir = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/hek293/chip/tf"
tcf7l2_dir = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/hek293/chip/"
ep300_hela_dir = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/hela/chip/tf/"
ep300_k562_dir = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/k562/chip/tf/"
tcf7l2_liftover_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/hek293/chip/TCF7L2/ENCSR000EUY/ENCFF002CRP.bed.gz"
ep300_hela_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/hela/chip/tf/EP300/ENCSR680OFU/ENCFF979KQB.bed.gz"
ep300_k562_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/k562/chip/tf/EP300/ENCSR000EGE/ENCFF433PKW.bed.gz"
save_master_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/master/master.bed"

tfs_of_interest = [
    "PRDM6", "FEZF1", "FOXA1", "WT1", "PRDM4", "SP7", "CTBP1", "ZEB2", "ZNF423", "SP1",
    "PATZ1", "GLIS1", "SCRT1", "ATF2", "LEF1", "YY1", "SP2", "CTCF", "TCF7L2", "SUZ12", 
    "CHD8", "BAF", "EP300",  
    ]

def create_master_list(
    h3k4me1_file, h3k27ac_file, 
    tss_file, 
    tf_dir, tcf7l2_dir, ep300_hela_dir, ep300_k562_dir, tcf7l2_liftover_file, ep300_hela_file, ep300_k562_file, tfs_of_interest, 
    save_master_file):
    # create union of histone bed files
    h3k4me1_bed = pybedtools.BedTool(h3k4me1_file).sort()
    h3k27ac_bed = pybedtools.BedTool(h3k27ac_file).sort()
    histone_union = h3k4me1_bed.cat(h3k27ac_bed, postmerge=True, c=(4,5), o=("collapse", "collapse"))
    # remove tss sites from histone union
    tss_bed = pybedtools.BedTool(tss_file).sort()
    histone_no_tss = histone_union.intersect(tss_bed, v=True)
    # overlap histone with tf binding sites
    encode_tf_data = [f.path for tf in os.scandir(tf_dir) for exp in os.scandir(tf.path) for f in os.scandir(exp.path) if f.path.endswith(".bed.gz")]
    encode_tf_data.extend([tcf7l2_liftover_file, ep300_hela_file, ep300_k562_file])
    inter_tf = histone_no_tss.intersect(encode_tf_data, wo=True, filenames=True)
    inter_merged = inter_tf.merge(c=(4,6), o=("distinct", "collapse"))
    # remove sites with less than 1 tf binding site apart from the tfs of interest
    df = inter_merged.to_dataframe()
    ## remove file prefix and suffix
    df["score"] = df["score"].str.replace(tf_dir, "")
    df["score"] = df["score"].str.replace(".bed.gz", "", regex=False)
    df["score"] = df["score"].str.replace(tcf7l2_dir, "")
    df["score"] = df["score"].str.replace(ep300_hela_dir, "")
    df["score"] = df["score"].str.replace(ep300_k562_dir, "")
    df_score_len = df.score.apply(lambda x: len(x.split(",")))
    df["tf_num"] = df_score_len
    df_to_keep = df.loc[df.score.str.contains("|".join(tfs_of_interest), regex=True)]
    df_to_further_filter = df.loc[~df.score.str.contains("|".join(tfs_of_interest), regex=True)]
    df_filtered = df_to_further_filter.loc[df_to_further_filter.tf_num>1]
    df_multi_tf = pd.concat((df_to_keep, df_filtered))
    # only keep known chromosomes
    known_chrms = [
        'chr1', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15',
        'chr16', 'chr17', 'chr18', 'chr19', 'chr2', 'chr20', 'chr21',
        'chr22', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9',
        'chrX', 'chrY'
        ]
    df_multi_tf = df_multi_tf.loc[df_multi_tf.chrom.isin(known_chrms)]
    # pad regions less than 500 bp to 500 bp, if diff is odd, add bigger half at the end
    df_diff = 500 - (df_multi_tf["end"] - df_multi_tf["start"])
    df_multi_tf.loc[df_diff>0, "start"] -= np.floor(df_diff.loc[df_diff>0]/2)
    df_multi_tf.loc[df_diff>0, "end"] += np.ceil(df_diff.loc[df_diff>0]/2)
    df_multi_tf["start"] = df_multi_tf["start"].astype(int)
    df_multi_tf["end"] = df_multi_tf["end"].astype(int)
    # convert to bed and save
    df_multi_tf_bed = pybedtools.BedTool.from_dataframe(df_multi_tf).sort()
    df_multi_tf_bed.moveto(save_master_file)
    pybedtools.helpers.cleanup()
    return


if __name__ == "__main__":
    
    create_master_list(
        h3k4me1_file, h3k27ac_file, 
        tss_file, 
        tf_dir, tcf7l2_dir, ep300_hela_dir, ep300_k562_dir, tcf7l2_liftover_file, ep300_hela_file, ep300_k562_file, tfs_of_interest, 
        save_master_file)
