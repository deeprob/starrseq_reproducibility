import os
import numpy as np
import pandas as pd
import pybedtools
import pysam
import json
from argparse import Namespace
import itertools
import functools
import multiprocessing as mp
from pybedtools.featurefuncs import greater_than

# TODO: take tmp dir from arguments
pybedtools.helpers.set_tempdir("/data5/deepro/tmp/")


###############################
# read meta file; create args #
###############################

def create_args(meta_file, lib_name):
    with open(meta_file, "r") as f: 
        meta_dict = json.load(f)
        
    args = Namespace(
        # from metadata file
        library_prefix = meta_dict[lib_name]["prefix"],
        library_reps = meta_dict[lib_name]["replicates"],
        library_pair= meta_dict[lib_name]["read_pairs"],
        library_umi = meta_dict[lib_name]["umi"],
        library_suffix = meta_dict[lib_name]["suffix"],
        library_short = meta_dict[lib_name]["shortform"],
        reference_genome = meta_dict["genome"]["ref_fasta"],
        reference_genome_twobit = meta_dict["genome"]["ref_twobit"],
        genome_sizes = meta_dict["genome"]["chrom_sizes"],
        roi_file = meta_dict["roi"]["sorted"],
        roi_window_file = meta_dict["roi"]["window"],
    )

    return args


####################
# Filename parsing #
####################

def get_statistics_filepath(storage_dir, lib_short):
    filename = os.path.join(storage_dir, "table", lib_short, "stats.csv")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return filename

def get_analyzed_filename_suffix(analysis):
    suffix_dict = {
        "deduped_starrdust": ".fastq",
        "deduped_picard": ".bam", 
        "aligned": ".bam", 
        "filtered": ".bam"
        }
    lib_suffix_formatted = suffix_dict[analysis]
    return lib_suffix_formatted

def join_names(iter1, iter2):
    if iter2:
        return ["_".join(fi) for fi in itertools.product(iter1, iter2)]
    return iter1

def add_suffix(filenames, lib_suffix):
    return list(map(lambda x: x + lib_suffix, filenames))

def get_analyzed_filenames(lib_prefix, lib_reps, lib_pairs, lib_suffix):
    filenames = add_suffix(functools.reduce(join_names, [[lib_prefix], lib_reps.split(), lib_pairs.split()]), lib_suffix)
    return filenames

def remove_prefix_suffix(filename, prefix, suffix):
    return filename.replace(prefix, "").replace(suffix, "").strip("_")

def get_analyzed_filepaths(dir_path, lib_short, filename):
    return os.path.join(dir_path, lib_short, filename)

def get_depth_bed_filepaths(store_dir, lib_short, lib_prefix, lib_rep):
    return os.path.join(store_dir, "cov", lib_short, f"{lib_prefix}_{lib_rep}.bed")

def get_lib_depth_beds_filepaths(store_dir, lib_short, lib_prefix, lib_reps):
    depth_beds = [get_depth_bed_filepaths(store_dir, lib_short, lib_prefix, lib_rep) for lib_rep in lib_reps.split()]
    return depth_beds

##############
# ROI create #
##############

def get_unique_fragments(in_bam, out_bed):
    """
    Breaks the genome into non-overlapping windows
    """
    # convert bam to bed
    uniq_frag_bed = pybedtools.BedTool().merge(i=in_bam)
    os.makedirs(os.path.dirname(out_bed), exist_ok=True)
    uniq_frag_bed.moveto(out_bed)
    return
    
###########
# Read QC #
###########

def get_roi_info(roi_file):
    df_roi = pd.read_csv(roi_file, sep="\t", header=None)
    roi_num = len(df_roi)
    roi_total_bps = sum(df_roi.iloc[:,2].subtract(df_roi.iloc[:,1]))
    roi_meansize = roi_total_bps//roi_num
    return roi_num, roi_meansize, roi_total_bps

def get_num_reads_fastq(read_file):
    val = pysam.view("-c", read_file)    
    return int(val.strip())

def get_num_reads_bam_pair1(bam_file):
    # val = pysam.view("-c", bam_file)
    # read mapped in proper pair and first in pair :: https://broadinstitute.github.io/picard/explain-flags.html
    val = pysam.view("-f", "66", "-c", bam_file)
    return int(val.strip())

def get_num_reads_bam_pair2(bam_file):
    # val = pysam.view("-c", bam_file)
    # read mapped in proper pair and second in pair :: https://broadinstitute.github.io/picard/explain-flags.html
    val = pysam.view("-f", "130", "-c", bam_file)
    return int(val.strip())

def get_coverage(num_reads, len_region, read_length=150, pe=True):
    factor = 2 if pe else 1
    coverage = (num_reads*read_length*factor)/len_region
    return int(coverage)

def get_roi_depth(filtered_bam, roi_sorted_bed, bed_out):
    # bam = pybedtools.BedTool(filtered_bam)
    roi = pybedtools.BedTool(roi_sorted_bed)
    try:
        c = roi.coverage(filtered_bam, sorted=True)
    except Exception as e:
        c = roi.coverage(filtered_bam)
    os.makedirs(os.path.dirname(bed_out), exist_ok=True)
    c.moveto(bed_out)
    return

##################
# create windows #
##################

def make_windows(in_bed, out_bed, window_size=500, window_stride=50):
    """
    Break the ROIs into fragments of an user defined window size and stride
    """
    window = pybedtools.BedTool().window_maker(b=in_bed ,w=window_size, s=window_stride)
    window_df = window.to_dataframe()
    # get rid of windows which have the same end point
    last_end = None
    rows_to_omit = []
    for i, row in enumerate(window_df.itertuples()):
        if row.end == last_end:
            rows_to_omit.append(i)
        last_end = row.end
    window_df = window_df.loc[~window_df.index.isin(rows_to_omit)]
    os.makedirs(os.path.dirname(out_bed), exist_ok=True)
    window_df.to_csv(out_bed, sep="\t", header=None, index=None)
    return

def make_windows_faster(in_bed, out_bed, window_size=500, window_stride=50):
    """
    Break the ROIs into fragments of an user defined window size and stride
    """
    window = pybedtools.BedTool().window_maker(b=in_bed, w=window_size, s=window_stride)
    # only keep windows of length greater than w-s-1
    window_new_filtered = window.filter(greater_than, window_size - window_stride - 1)
    window_new_filtered.saveas(out_bed)
    return

################
# multiprocess #
################

def run_singleargs_pool_job(pool_function, pool_iter, threads=None):
    if not threads:
        threads = len(pool_iter)    
    pool = mp.Pool(threads)
    results = pool.map(pool_function, pool_iter)
    pool.close()
    pool.join()
    return results

def run_multiargs_pool_job(pool_function, pool_iter, threads=None):
    if not threads:
        threads = len(pool_iter)
    pool = mp.Pool(threads)
    results = pool.starmap(pool_function, pool_iter)
    pool.close()
    pool.join()
    return results
