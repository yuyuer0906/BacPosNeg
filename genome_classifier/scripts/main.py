#!/usr/bin/env python3
# scripts/main.py

import argparse
import os
import logging
from .run_prodigal import run_prodigal_on_folder
from .run_hmmsearch import run_hmmsearch_on_folder
from .process_hmm_results import process_hmmsearch_outputs
from .extract_features import extract_features
from .predict import make_predictions
from colorama import Fore, Style

def main():
    parser = argparse.ArgumentParser(description='Genome Classification Pipeline')
    parser.add_argument('-i', '--input_dir', required=True, help='Input directory containing genome files')
    parser.add_argument('-o', '--output_dir', required=True, help='Output directory for results')
    parser.add_argument('-c', '--completeness_file', required=True, help='CSV file containing genome completeness information')
    parser.add_argument('-t', '--threads', type=int, default=4, help="Number of CPU threads for HMMsearch (default: 4)")
    parser.add_argument('-p', '--prodigal_threads', type=int, default=4, help="Number of CPU threads for Prodigal (default: 4)")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    completeness_file = args.completeness_file
    hmm_threads = args.threads
    prodigal_threads = args.prodigal_threads
    
    os.makedirs(output_dir, exist_ok=True)

    try:
        print("Running Prodigal...")
        predicted_proteins_dir = os.path.join(output_dir, 'predicted_proteins')
        os.makedirs(predicted_proteins_dir, exist_ok=True)
        run_prodigal_on_folder(input_dir, predicted_proteins_dir, num_threads=prodigal_threads)

        print("Running HMMsearch...")
        hmmsearch_results_dir = os.path.join(output_dir, 'hmmsearch_results')
        os.makedirs(hmmsearch_results_dir, exist_ok=True)
        run_hmmsearch_on_folder(predicted_proteins_dir, hmmsearch_results_dir, num_cpus=hmm_threads)

        print("Processing HMMsearch outputs...")
        processed_results_dir = os.path.join(output_dir, 'processed_results')
        os.makedirs(processed_results_dir, exist_ok=True)
        process_hmmsearch_outputs(hmmsearch_results_dir, processed_results_dir)

        print("Extracting features...")
        features_file = os.path.join(output_dir, 'features.csv')
        extract_features(processed_results_dir, predicted_proteins_dir, features_file)

        print("Making predictions...")
        predictions_file = os.path.join(output_dir, 'predictions.csv')
        make_predictions(features_file, completeness_file, predictions_file)

        print(f"Pipeline completed. Predictions are saved in {predictions_file}")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        exit(1)

if __name__ == '__main__':
    main()
