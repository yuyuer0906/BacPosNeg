# scripts/run_hmmsearch.py

import os
from .utils import run_command, list_files, create_directory, get_base_name

def run_hmmsearch_on_folder(input_dir, output_dir, num_cpus=4):
    create_directory(output_dir)
    markers_hmm = 'genome_classifier/data/markers.hmm'  # Path to markers.hmm file
    if not os.path.exists(markers_hmm):
        raise FileNotFoundError("markers.hmm file not found in data directory.")
    
    faa_files = list_files(input_dir, extensions=['.faa'])
    if not faa_files:
        raise FileNotFoundError("No predicted protein files found for HMMsearch.")
    
    for filename in faa_files:
        input_file = os.path.join(input_dir, filename)
        base_name = get_base_name(filename)
        output_file = os.path.join(output_dir, f"{base_name}_hmmsearch.tbl")
        cmd = f"hmmsearch --cpu {num_cpus} -E 1e-5 --tblout {output_file} {markers_hmm} {input_file}"
        run_command(cmd)
