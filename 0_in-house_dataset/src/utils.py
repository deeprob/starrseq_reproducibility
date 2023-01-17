import os
import requests
import argparse
import multiprocessing as mp
from itertools import starmap

########################
# encode download data #
########################


def get_search_dict(url):
    # Force return from the server in JSON format
    headers = {'accept': 'application/json'}

    # GET the search result
    response = requests.get(url, headers=headers)

    # Extract the JSON response as a python dictionary
    search_results = response.json()
    return search_results


def get_file_annotations(search_file_dict):
    file_format = search_file_dict.get("file_format", "")
    file_format_type = search_file_dict.get("file_format_type", "")
    default = search_file_dict.get("preferred_default", False)
    analysis = search_file_dict.get("analyses", "")
    if analysis:
        if type(analysis) == list:
            if type(analysis[0]) == dict:
                analysis = analysis[0].get("title", "")
    file_type = search_file_dict.get("output_type", "")
    return file_format, file_format_type, default, analysis, file_type


def check_file_annotations(
    file_annotations, 
    fformat, fformat_type, 
    isdefault, analysis_pipe, 
    assembly, f_type 
    ):
    file_format, file_format_type, default, analysis, file_type =  file_annotations
    try:
        assert file_format == fformat
        assert file_format_type == fformat_type
        assert default == isdefault
        assert analysis_pipe in analysis
        assert assembly in analysis
        if f_type:
            assert file_type == f_type
    except AssertionError:
        return False
    return True


def get_cloud_metadata(search_file_dict):
    return search_file_dict["cloud_metadata"]


def get_metadata(
    file_id, 
    fformat, fformat_type, 
    isdefault, analysis_pipe, 
    assembly, f_type
    ):
    search_file_url = f"https://www.encodeproject.org{file_id}"
    search_file_dict = get_search_dict(search_file_url)
    if check_file_annotations(get_file_annotations(search_file_dict), fformat, fformat_type, isdefault, analysis_pipe, assembly, f_type):
        return get_cloud_metadata(search_file_dict)
    return None


def download_file(metadata, file_prefix):
    url = metadata["url"]
    filename = os.path.join(file_prefix, os.path.basename(url))
    if os.path.exists(filename):
        # TODO: change to logger
        print(f"Warning: File {filename} already exists")
    file = open(filename, "wb")
    response = requests.get(url)
    assert response.status_code == 200
    file.write(response.content)
    return filename


def get_narrowpeak_bed(
    single_exp_dict, root_dir, 
    fformat, fformat_type, 
    isdefault, analysis_pipe, 
    assembly, file_type 
    ):
    # chip seq target
    target = single_exp_dict["target"]["label"]
    # experiment accession number
    accession = single_exp_dict["accession"]
    # all available file ids
    files = [f["@id"] for f in single_exp_dict["files"]]
    # get metadata list for all available file ids after checking for annotations
    map_iter = [(f, fformat, fformat_type, isdefault, analysis_pipe, assembly, file_type) for f in files]
    metadata_list = list(starmap(get_metadata, map_iter))
    filtered_metadata_list = [m for m in metadata_list if m]
    # there should be a single file if the file annotations check out and a cloud metadata is obtained
    if len(filtered_metadata_list) ==  1:
        # make proper directory structure
        storage_dir = os.path.join(root_dir, target, accession)
        os.makedirs(storage_dir,  exist_ok=True)
        # download bed file
        downloaded_file = download_file(filtered_metadata_list[0], storage_dir)
        return downloaded_file
    # if there are 0 files return None
    return

  


