# scripts/process_hmm_results.py

import os
import pandas as pd
from .utils import create_directory

def process_hmmsearch_outputs(input_dir, output_dir):
    create_directory(output_dir)
    all_marker_counts = {}
    tbl_files = [f for f in os.listdir(input_dir) if f.endswith('_hmmsearch.tbl')]
    if not tbl_files:
        raise FileNotFoundError("No HMMsearch output files found.")
    for filename in tbl_files:
        input_file = os.path.join(input_dir, filename)
        base_name = filename.replace('_hmmsearch.tbl', '')
        counts = parse_hmmsearch_table(input_file)
        all_marker_counts[base_name] = counts

    # Combine counts into a DataFrame
    df = pd.DataFrame.from_dict(all_marker_counts, orient='index').fillna(0)
    df.index.name = 'Genome'
    df.reset_index(inplace=True)

    # Save to CSV with marker names as headers
    output_csv = os.path.join(output_dir, 'combined_marker_counts.csv')
    df.to_csv(output_csv, index=False)

def parse_hmmsearch_table(filepath):
    counts = {}
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            fields = line.strip().split()
            target_name = fields[0]  # target sequence name
            query_name = fields[2]   # HMM (marker) name
            # You might want to filter based on E-value or other criteria here

            # Increment count for the marker (query_name)
            counts[query_name] = counts.get(query_name, 0) + 1
    return counts
