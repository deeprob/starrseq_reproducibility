import os
import itertools as it
import numpy as np
import pandas as pd
import pyliftover


chain_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/liftover/hg19ToHg38.over.chain.gz"
liftover_file = "/data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/data/encode/hek293/chip/TCF7L2/ENCSR000EUY/ENCFF002CRP.narrowPeak.gz"
save_file = liftover_file.replace("narrowPeak", "bed")


def remap_coords(chain_file, liftover_file, save_file):
    # read file to liftover
    df = pd.read_csv(liftover_file, sep="\t", header=None)
    # create liftover object
    lo = pyliftover.LiftOver(chain_file)
    # get start and end coords from liftover file
    start_coord_iter = list(zip(df[0], df[1]))
    end_coord_iter = list(zip(df[0], df[2]))
    # convert the start and end coords
    hg38_start_coords= list(it.starmap(lo.convert_coordinate, start_coord_iter))
    hg38_end_coords= list(it.starmap(lo.convert_coordinate, end_coord_iter))
    # create a new dataframe with start and end coords
    chrm_sa, starta, chrm_ea, enda = [], [], [], []
    for i,j in zip(hg38_start_coords, hg38_end_coords):
        if len(i)==1:
            chrm_s = i[0][0]
            start = i[0][1]
        else:
            chrm_s = ""
            start = np.nan
        if len(j)==1:
            chrm_e = j[0][0]
            end = j[0][1]
        else:
            chrm_e = ""
            end = np.nan
        chrm_sa.append(chrm_s)
        chrm_ea.append(chrm_e)
        starta.append(start)
        enda.append(end)
    new_df = pd.DataFrame()
    new_df["chrm_s"] = chrm_sa
    new_df["chrm_e"] = chrm_ea
    new_df["start"] = starta
    new_df["end"] = enda
    # parse the dataframe to get rid of incorrect/unavailable chromosomes
    parsed_df = new_df.loc[new_df.chrm_s==new_df.chrm_e]
    parsed_df = parsed_df.drop(columns=["chrm_e"]).rename(columns={"chrm_s": "chrom"})
    parsed_df["start"] = parsed_df.start.astype(int)
    parsed_df["end"] = parsed_df.end.astype(int)
    parsed_df = parsed_df.loc[parsed_df.start<parsed_df.end]
    parsed_df = pd.concat((parsed_df, df.iloc[:, 3:]), join="inner", axis=1)
    # save the parsed df in save file
    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    parsed_df.to_csv(save_file, sep="\t", header=False, index=False)
    return


if __name__ == "__main__":
    remap_coords(chain_file, liftover_file, save_file)
