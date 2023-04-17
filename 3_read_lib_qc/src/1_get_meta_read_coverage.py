# make a meta read coverage file by calculating the read depth of 
# all the regions across all libraries

import argparse
import os
import utils as ut
import pandas as pd

def main(
    cov_dir,
    store_dir,
    libs_prefix,
    libs_reps,
    libs_short,
    ):

    lib_cov_dfs = []
    for pre, reps, short in zip(libs_prefix, libs_reps, libs_short):
        lib_beds = ut.get_lib_depth_beds_filepaths(cov_dir, short, pre, reps)
        lib_df = pd.concat(list(map(ut.read_and_extract_depth, lib_beds)), axis=1)
        lib_df.columns = [f"{short.upper()}_R{i}" for i in range(1, len(lib_beds)+1)] 
        lib_cov_dfs.append(lib_df)
    # store coverage dfs
    cov_filename = os.path.join(store_dir, "cov", "meta_cov.csv")
    lib_cov_meta_df = pd.concat(lib_cov_dfs, axis=1)
    lib_cov_meta_df.to_csv(cov_filename, index=False)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STARRSeq analysis")
    parser.add_argument("meta_file", type=str, help="The meta json filepath where library information is stored")
    parser.add_argument("cov_dir", type=str, help="Directory where the read files are stored")
    parser.add_argument("store_dir", type=str, help="Output files dir")
    parser.add_argument("--libs", type=str, help="The library name as given in the meta file", nargs="+", default=["input"])

    cli_args = parser.parse_args()
    lib_args = [ut.create_args(cli_args.meta_file,lib) for lib in cli_args.libs]

    main(
        cli_args.cov_dir,
        cli_args.store_dir,
        [lib.library_prefix for lib in lib_args],
        [lib.library_reps for lib in lib_args],
        [lib.library_short for lib in lib_args],
    )
