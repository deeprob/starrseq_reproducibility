import pandas as pd


refseq_gene_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/tss/Refseq_hg38_gene_coordinates.txt"
save_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/tss/refseq_gene_tss_2kb.bed"

def create_tss_file(refseq_gene_file, save_file):
    df = pd.read_csv(refseq_gene_file, sep="\t")
    df_neg_strand = df.loc[df.strand=="-"]
    df_pos_strand = df.loc[df.strand=="+"]
    df_pos,df_neg = pd.DataFrame(), pd.DataFrame()
    df_pos["chrom"] = df_pos_strand["chrom"]
    df_pos["start"] = df_pos_strand["txStart"] - 2000
    df_pos["end"] = df_pos_strand["txStart"] + 2000
    df_pos["site"] = df_pos_strand["chrom"] + ":" + df_pos_strand["txStart"].astype(str)


    df_neg["chrom"] = df_neg_strand["chrom"]
    df_neg["start"] = df_neg_strand["txEnd"] - 2000
    df_neg["end"] = df_neg_strand["txEnd"] + 2000
    df_neg["site"] = df_neg_strand["chrom"] + ":" + df_neg_strand["txEnd"].astype(str)


    df_tss = pd.concat((df_pos, df_neg), axis=0).sort_values(["chrom", "start", "end"]).drop_duplicates()
    df_tss["start"] = df_tss["start"].clip(lower=0)
    df_tss.to_csv(save_file, sep="\t", header=False, index=False)


if __name__ == "__main__":
    create_tss_file(refseq_gene_file, save_file)
    