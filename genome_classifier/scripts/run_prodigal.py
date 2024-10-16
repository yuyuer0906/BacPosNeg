# scripts/run_prodigal.py


import os
from .utils import run_command, list_files, create_directory, get_base_name

def run_prodigal_on_folder(input_dir, output_dir):
    create_directory(output_dir)
    fasta_files = list_files(input_dir, extensions=['.fasta', '.fa', '.fna'])
    if not fasta_files:
        raise FileNotFoundError("No genome files found in the input directory.")
    for filename in fasta_files:
        input_file = os.path.join(input_dir, filename)
        base_name = get_base_name(filename)
        output_file = os.path.join(output_dir, f"{base_name}.faa")
        cmd = f"prodigal -i {input_file} -a {output_file} -q"
        run_command(cmd)
