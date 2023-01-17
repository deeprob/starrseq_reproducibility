import argparse
import multiprocessing as mp
import utils as ut


def main(
    web_url, storage_dir,
    fformat="bed", fformat_type="narrowPeak", 
    isdefault=True, analysis_pipe="ENCODE3", assembly="GRCh38", file_type=""
    ):
    main_search_results = ut.get_search_dict(web_url)
    # replace the underscores with spaces ; required for argparse inputs which cannot handle spaces
    file_type = file_type.replace("_", " ")
    # the "@graph" key has the search results as a list
    pool_iter = [
        (md, storage_dir, fformat, fformat_type, isdefault, analysis_pipe, assembly, file_type) for md in main_search_results["@graph"]
        ]
    pool = mp.Pool(len(pool_iter))
    pool.starmap(ut.get_narrowpeak_bed, pool_iter) 
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="download data from encode")
    parser.add_argument("encode_url", type=str, help="The encode search url which returns a list of experiments of interest")
    parser.add_argument("storage_dir", type=str, help="dir to store results")
    parser.add_argument("analysis", type=str, help="ENCODE analysis pipeline used")
    parser.add_argument("assembly", type=str, help="Genome assembly used")
    parser.add_argument("--default", help="default status of file", action="store_true")
    parser.add_argument("--ftype", type=str, help="The type of output file, use _ instead of spaces", default="")
    args = parser.parse_args()

    main(args.encode_url, args.storage_dir, analysis_pipe=args.analysis, isdefault=args.default, assembly=args.assembly, file_type=args.ftype)
