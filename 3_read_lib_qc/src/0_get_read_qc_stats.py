import argparse
import utils as ut
from itertools import starmap
import os


def main(
    raw_data_dir,
    aligned_data_dir,
    deduped_data_dir,
    filtered_data_dir,
    storage_dir,
    library_prefix, 
    library_replicates, 
    library_read_pairs,
    library_suffix,
    roi_file,
    library_short,
    read_length,
    dedup_tool,
    calculate_depth,
    cores,
    ):
    # if roi file is not given, make an roi file - making roi file from input bam file and using it for output libaries is recommended
    if not roi_file:
        input_bam = os.path.join(filtered_data_dir, library_short, f"{library_prefix}.bam")
        roi_file = os.path.join(filtered_data_dir, library_short, "roi_file.bed")
        ut.get_unique_fragments(input_bam, roi_file)
    # statistics_file
    stats_filepath = ut.get_statistics_filepath(storage_dir, library_short)
    stats_file = open(stats_filepath, "w")
    # roi statistics
    roi_num, roi_meansize, roi_total_bps = ut.get_roi_info(roi_file)
    stats_file.write(f"roi_stats,roi_num,{roi_num}\n")
    stats_file.write(f"roi_stats,roi_meansize,{roi_meansize}\n")
    stats_file.write(f"roi_stats,roi_total_bps,{roi_total_bps}\n")
    # raw data statistics
    raw_data_suff = library_suffix
    raw_data_filenames = ut.get_analyzed_filenames(library_prefix, library_replicates, library_read_pairs, raw_data_suff)
    raw_data_filepaths = [ut.get_analyzed_filepaths(raw_data_dir, library_short, fn) for fn in raw_data_filenames]
    raw_file_reads = ut.run_singleargs_pool_job(ut.get_num_reads_fastq, raw_data_filepaths, threads=cores)
    raw_data_filenames_parsed = [ut.remove_prefix_suffix(fn, library_prefix, raw_data_suff) for fn in raw_data_filenames]
    for rfn, rfr in zip(raw_data_filenames_parsed, raw_file_reads):
        stats_file.write(f"raw_reads,{rfn},{rfr}\n")
    # aligned data statistics
    aligned_data_suff = ut.get_analyzed_filename_suffix("aligned")
    aligned_data_filenames = ut.get_analyzed_filenames(library_prefix, library_replicates, "", aligned_data_suff)
    aligned_data_filepaths = [ut.get_analyzed_filepaths(aligned_data_dir, library_short, fn) for fn in aligned_data_filenames]
    aligned_file_reads_pair1 = ut.run_singleargs_pool_job(ut.get_num_reads_bam_pair1, aligned_data_filepaths, threads=cores)
    aligned_file_reads_pair2 = ut.run_singleargs_pool_job(ut.get_num_reads_bam_pair2, aligned_data_filepaths, threads=cores)
    aligned_data_filenames_parsed = [ut.remove_prefix_suffix(fn, library_prefix, aligned_data_suff) for fn in aligned_data_filenames]
    for ffn, ffr in zip(aligned_data_filenames_parsed, aligned_file_reads_pair1):
        stats_file.write(f"aligned_reads_pair1,{ffn},{ffr}\n")
    for ffn, ffr in zip(aligned_data_filenames_parsed, aligned_file_reads_pair2):
        stats_file.write(f"aligned_reads_pair2,{ffn},{ffr}\n")
    # deduped data statistics
    deduped_data_suff = ut.get_analyzed_filename_suffix(f"deduped_{dedup_tool}")
    if dedup_tool=="picard":
        deduped_data_filenames = ut.get_analyzed_filenames(library_prefix, library_replicates, "", deduped_data_suff)
        deduped_data_filepaths = [ut.get_analyzed_filepaths(deduped_data_dir, library_short, fn) for fn in deduped_data_filenames]
        deduped_file_reads_pair1 = ut.run_singleargs_pool_job(ut.get_num_reads_bam_pair1, deduped_data_filepaths, threads=cores)
        deduped_file_reads_pair2 = ut.run_singleargs_pool_job(ut.get_num_reads_bam_pair2, deduped_data_filepaths, threads=cores)
        deduped_data_filenames_parsed = [ut.remove_prefix_suffix(fn, library_prefix, deduped_data_suff) for fn in deduped_data_filenames]
        for ffn, ffr in zip(deduped_data_filenames_parsed, deduped_file_reads_pair1):
            stats_file.write(f"deduped_reads_pair1,{ffn},{ffr}\n")
        for ffn, ffr in zip(deduped_data_filenames_parsed, deduped_file_reads_pair2):
            stats_file.write(f"deduped_reads_pair2,{ffn},{ffr}\n")
    elif dedup_tool=="starrdust":
        deduped_data_filenames = ut.get_analyzed_filenames(library_prefix, library_replicates, library_read_pairs, deduped_data_suff)
        deduped_data_filepaths = [ut.get_analyzed_filepaths(deduped_data_dir, library_short, fn) for fn in deduped_data_filenames]
        deduped_file_reads = ut.run_singleargs_pool_job(ut.get_num_reads_fastq, deduped_data_filepaths, threads=cores)
        deduped_data_filenames_parsed = [ut.remove_prefix_suffix(fn, library_prefix, deduped_data_suff) for fn in deduped_data_filenames]
        for ffn, ffr in zip(deduped_data_filenames_parsed, deduped_file_reads):
            stats_file.write(f"deduped_reads,{ffn},{ffr}\n")
    # filtered data statistics
    filtered_data_suff = ut.get_analyzed_filename_suffix("filtered")
    filtered_data_filenames = ut.get_analyzed_filenames(library_prefix, library_replicates, "", filtered_data_suff)
    filtered_data_filepaths = [ut.get_analyzed_filepaths(filtered_data_dir, library_short, fn) for fn in filtered_data_filenames]
    filtered_file_reads_pair1 = ut.run_singleargs_pool_job(ut.get_num_reads_bam_pair1, filtered_data_filepaths, threads=cores)
    filtered_file_reads_pair2 = ut.run_singleargs_pool_job(ut.get_num_reads_bam_pair2, filtered_data_filepaths, threads=cores)
    filtered_data_filenames_parsed = [ut.remove_prefix_suffix(fn, library_prefix, filtered_data_suff) for fn in filtered_data_filenames]
    for ffn, ffr in zip(filtered_data_filenames_parsed, filtered_file_reads_pair1):
        stats_file.write(f"filtered_reads_pair1,{ffn},{ffr}\n")
    for ffn, ffr in zip(filtered_data_filenames_parsed, filtered_file_reads_pair2):
        stats_file.write(f"filtered_reads_pair2,{ffn},{ffr}\n")
    # library coverage
    coverage_iter = [(freads, roi_total_bps, read_length, True) for freads in filtered_file_reads_pair1]
    filtered_files_coverage = list(starmap(ut.get_coverage, coverage_iter))
    for ffn, c in zip(filtered_data_filenames_parsed, filtered_files_coverage):
        stats_file.write(f"coverage,{ffn},{c}\n")
    stats_file.close()
    if calculate_depth:
        # library depth bed creation
        depth_bed_filepaths = list(starmap(ut.get_depth_bed_filepaths, [(storage_dir, library_short, library_prefix, rep) for rep in library_replicates.split()]))
        depth_iter = [(fp, roi_file, bo) for fp,bo in zip(filtered_data_filepaths, depth_bed_filepaths)]
        ut.run_multiargs_pool_job(ut.get_roi_depth, depth_iter, threads=cores)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STARRSeq analysis")
    parser.add_argument("meta_file", type=str, help="The meta json filepath where library information is stored")
    parser.add_argument("lib", type=str, help="The library name as given in the meta file")
    parser.add_argument("raw_data_dir", type=str, help="raw data files dir")
    parser.add_argument("aligned_data_dir", type=str, help="aligned data files dir")
    parser.add_argument("deduped_data_dir", type=str, help="deduped data files dir")
    parser.add_argument("filtered_data_dir", type=str, help="filtered data files dir")
    parser.add_argument("store_dir", type=str, help="Output files dir")
    parser.add_argument("-r", "--roi_file", type=str, default="", help="Roi file path") 
    parser.add_argument("-l", "--read_length", type=int, default=150, help="Read length of sequencer :: used to calculate coverage")  
    parser.add_argument("-d", "--calculate_depth", action="store_true", help="Calculate library depth per region of interest")  
    parser.add_argument("-t", "--dedup_tool", type=str, default="starrdust", help="The deduplication tool used")
    parser.add_argument("-c", "--cores", type=int, default=32, help="Number of cores to parallelize tasks") 

    cli_args = parser.parse_args()
    lib_args = ut.create_args(cli_args.meta_file, cli_args.lib)

    if cli_args.roi_file:
        roi_file = cli_args.roi_file
    else:
        roi_file = lib_args.roi_file

    main(
        cli_args.raw_data_dir,
        cli_args.aligned_data_dir,
        cli_args.deduped_data_dir,
        cli_args.filtered_data_dir,
        cli_args.store_dir,
        lib_args.library_prefix, 
        lib_args.library_reps, 
        lib_args.library_pair,
        lib_args.library_suffix,
        roi_file,
        lib_args.library_short,
        cli_args.read_length,
        cli_args.dedup_tool,
        cli_args.calculate_depth,
        cli_args.cores,
    )
