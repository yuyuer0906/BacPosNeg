# This script is adapted from https://github.com/xinehc/ARGs_OAP
# Original code by Xiaole Yin, licensed under MIT.
# Modifications made to fit the requirements of the BacPosNeg project.

import os  
import subprocess  
import sys  
import glob  
import pandas as pd
 
from .settings import File, Setting, logger

class Prefilter:  
    def __init__(self, options):  
        self.__dict__.update(options)  
        self.setting = Setting(None, self.outdir)  
        self.db = self.setting.nps  
        self.check_input_output_dirs()  
  
    def check_input_output_dirs(self):  
        if not os.path.isdir(self.indir):  
            logger.critical(f'Input folder <{self.indir}> does not exist. Please check input folder.')  
            sys.exit(2)  
  
        self.files = glob.glob(os.path.join(self.indir, f'*.{self.format}')) + glob.glob(os.path.join(self.indir, f'*.{self.format}.gz'))  
        if not self.files:  
            logger.critical(f'No files found in input folder <{self.indir}>. Please check input folder or format.')  
            sys.exit(2)  
  
        if self.indir == self.outdir:  
            logger.critical('Input and output folders cannot be identical.')  
            sys.exit(2)  
        
    def delete_existing_file(self):
        # create the output directory if it doesn't exist
        os.makedirs(self.outdir, exist_ok=True)

        # path to the extracted.fa file in the output directory
        exist_file = os.path.join(self.outdir, 'extracted.fa')  

        if os.path.isfile(exist_file):  
            logger.warning(f'Output folder contains {exist_file}, it will be overwritten.')  
            try:  
                os.remove(exist_file)  
            except OSError as e:  
                logger.error(f'Failed to delete {exist_file}: {e}') 
  
    def extract_seqs(self, file):  
        self.run_diamond(file)  
        self.merge_sequences(file)  
   
    def run_diamond(self, file):  
        subprocess.run([  
            'diamond', 'blastx',  
            '--db', f'{self.db}.dmnd',  
            '--query', file.file,  
            '--out', file.tmp_seqs_txt,  
            '--outfmt', '6', 'qseqid', 'full_qseq',  
            '--evalue', '10',  
            '--id', '60',  
            '--query-cover', '15',  
            '--max-hsps', '1',  
            '--max-target-seqs', '1',  
            '--threads', str(self.thread),  
            '--quiet'  
        ], check=True, stderr=subprocess.PIPE)  
    
    def merge_sequences(self, file):  
        df = pd.read_table(file.tmp_seqs_txt, header=None, names=['qseqid', 'full_qseq'])  
        df = df.drop_duplicates(subset='qseqid')
        output_file = os.path.join(self.outdir, f'{file.sample_name}_extracted.fa')

        with open(output_file, 'a') as f:  
            for cnt, (qseqid, full_qseq) in enumerate(df.values, start=1):  
                f.write(f'>{file.sample_name}@{file.file_name}@{cnt}@{qseqid}\n{full_qseq}\n')

        with open(self.setting.extracted, 'a') as f:
            for cnt, (qseqid, full_qseq) in enumerate(df.values, start=1):
                f.write(f'>{file.sample_name}@{file.file_name}@{cnt}@{qseqid}\n{full_qseq}\n')
  
    def run(self):
        # Call delete_existing_file before processing
        self.delete_existing_file()

        for i, file_path in enumerate(sorted(self.files)):  
            logger.info(f'Processing <{file_path}> ({i + 1}/{len(self.files)})...')  
            file = File(file_path, self.outdir, self.format)  
            try:  
                self.extract_seqs(file)  
            except subprocess.CalledProcessError as e:  
                logger.warning(f'Something is wrong with <{file.file}>, skip.')  
                logger.error(f'Error message from Diamond:\n{e.stderr.decode()}')

            if not getattr(self, 'keep', False):    
                for tmp in glob.glob(os.path.join(self.outdir, '*.tmp')):  
                    os.remove(tmp)  
  
        logger.info('Finished extracting sequences.')
def run_prefilter(options):  
    Prefilter(vars(options)).run()
