# scripts/run_prodigal.py

import os
from concurrent.futures import ThreadPoolExecutor
from .utils import run_command, list_files, create_directory, get_base_name

def run_prodigal_on_folder(input_dir, output_dir, num_threads=4):
    """
    Run Prodigal on multiple files concurrently.
    
    :param input_dir: Directory containing input genome files.
    :param output_dir: Directory to save the output files.
    :param num_threads: Number of threads to use for concurrent processing.
    """
    create_directory(output_dir)
    fasta_files = list_files(input_dir, extensions=['.fasta', '.fa', '.fna'])
    
    if not fasta_files:
        raise FileNotFoundError("No genome files found in the input directory.")
    
    # Define a function to run Prodigal for a single file
    def run_prodigal(file):
        input_file = os.path.join(input_dir, file)
        base_name = get_base_name(file)
        output_file = os.path.join(output_dir, f"{base_name}.faa")
        cmd = f"prodigal -i {input_file} -a {output_file} -q"
        run_command(cmd)

    # Use ThreadPoolExecutor to run Prodigal concurrently
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(run_prodigal, fasta_files)
