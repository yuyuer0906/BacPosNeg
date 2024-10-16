# scripts/utils.py

import os
import sys
import subprocess


def create_directory(dir_path):
    """
    Create a directory if it doesn't exist.
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def list_files(directory, extensions=None):
    """
    List files in a directory with specific extensions.
    If extensions is None, all files are listed.
    """
    files = []
    for filename in os.listdir(directory):
        if extensions:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(filename)
        else:
            files.append(filename)
    return files

def get_base_name(file_path):
    """
    Get the base name of a file without extension.
    """
    return os.path.splitext(os.path.basename(file_path))[0]

def run_command(cmd):
    """
    Run a shell command and handle errors.
    """
    try:
        subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed with exit code {e.returncode}: {cmd}")

def read_fasta_sequences(fasta_file):
    """
    Generator to read sequences from a FASTA file.
    Yields tuples of (sequence_id, sequence).
    """
    with open(fasta_file, 'r') as f:
        seq_id = ''
        seq = ''
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if seq_id:
                    yield seq_id, seq
                seq_id = line[1:]
                seq = ''
            else:
                seq += line
        if seq_id:
            yield seq_id, seq

