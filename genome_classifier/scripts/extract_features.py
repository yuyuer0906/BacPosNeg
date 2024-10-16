# scripts/extract_features.py

import os
import numpy as np
import pandas as pd

def extract_features(processed_results_dir, predicted_proteins_dir, output_file):

    # Load marker counts
    counts_file = os.path.join(processed_results_dir, 'combined_marker_counts.csv')
    if not os.path.exists(counts_file):
        raise FileNotFoundError("Combined marker counts file not found.")
    df_counts = pd.read_csv(counts_file, index_col='Genome')

    # Load marker SPM list
    marker_spm_file = os.path.join('genome_classifier/data', 'marker_spm_list')
    if not os.path.exists(marker_spm_file):
        raise FileNotFoundError("marker_spm_list file not found in data directory.")
    marker_spm = pd.read_csv(marker_spm_file, sep='\s+', header=None, names=['Marker', 'SPM'])
    marker_spm_dict = marker_spm.set_index('Marker')['SPM'].to_dict()

    # Determine marker categories (negative or positive)
    marker_categories = {}
    for marker in marker_spm['Marker']:
        if marker.startswith('n_'):
            marker_categories[marker] = 'n'
        elif marker.startswith('p_'):
            marker_categories[marker] = 'p'
        else:
            continue

    # Initialize features DataFrame
    features = pd.DataFrame(index=df_counts.index)

    # For each genome, compute the features
    for genome in df_counts.index:
        genome_counts = df_counts.loc[genome]
        matched_markers = genome_counts[genome_counts > 0].index.tolist()

        n_marker_spm_values = []
        p_marker_spm_values = []
        n_marker_num = 0
        p_marker_num = 0

        for marker in matched_markers:
            spm_value = marker_spm_dict.get(marker)
            if spm_value is None:
                continue
            category = marker_categories.get(marker)
            if category == 'n':
                n_marker_spm_values.extend([spm_value] * int(genome_counts[marker]))
                n_marker_num += genome_counts[marker]
            elif category == 'p':
                p_marker_spm_values.extend([spm_value] * int(genome_counts[marker]))
                p_marker_num += genome_counts[marker]
            else:
                # Marker without category
                continue

        # Compute median SPM values
        n_marker_spm_median = np.median(n_marker_spm_values) if n_marker_spm_values else 0
        p_marker_spm_median = np.median(p_marker_spm_values) if p_marker_spm_values else 0

        # Compute total SPM values
        n_marker_spm_total = sum(n_marker_spm_values)
        p_marker_spm_total = sum(p_marker_spm_values)

        # Compute sigmoid difference
        difference = n_marker_spm_total - p_marker_spm_total
        sigmoid_difference = 1 / (1 + np.exp(-difference))

        # Compute gene_num (number of sequences)
        faa_file = os.path.join(predicted_proteins_dir, f"{genome}.faa")
        if os.path.exists(faa_file):
            gene_num = count_sequences_in_fasta(faa_file)
        else:
            gene_num = 0

        # Store features
        features.loc[genome, 'n_marker_spm_median'] = n_marker_spm_median
        features.loc[genome, 'p_marker_spm_median'] = p_marker_spm_median
        features.loc[genome, 'n_marker_num'] = n_marker_num
        features.loc[genome, 'p_marker_num'] = p_marker_num
        features.loc[genome, 'sigmoid(n_marker_spm_total-p_marker_spm_total)'] = sigmoid_difference
        features.loc[genome, 'gene_num'] = gene_num

    # Save features to CSV
    features.to_csv(output_file)

def count_sequences_in_fasta(fasta_file):
    count = 0
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                count += 1
    return count
