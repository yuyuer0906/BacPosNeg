# This script is adapted from https://github.com/xinehc/ARGs_OAP
# Original code by Xiaole Yin, licensed under MIT.
# Modifications made to fit the requirements of the BacPosNeg project.

import os  
import subprocess  
import sys  
import pandas as pd  
   
from .settings import Setting, logger  
from .utils import simple_count

class Finefilter:  
    def __init__(self, options):  
        # extract options  
        self.indir = options.get('indir', None)  
        self.outdir = options.get('outdir', None)  
        if self.outdir is None:  
            self.outdir = self.indir  
        else:  
            os.makedirs(self.outdir, exist_ok=True)
  
        self.blastout = options.get('blastout', None)    
        self.thread = options.get('thread', 8)
        
        self.setting = Setting(self.indir, self.outdir)    
        self.db = self.setting.nps
  
        # check input directory and required files
        if not os.path.isdir(self.indir):  
            logger.critical(f'Input folder <{self.indir}> does not exist. Please check input folder (-i/--indir).')  
            sys.exit(2)  
        
        if not os.path.isfile(self.setting.extracted):  
            logger.critical(f'File <extracted.fa> does not exist in <{self.indir}>. Please check input folder (-i/--indir).')  
            sys.exit(2)  
  
        # handle BLAST output option  
        if self.blastout is not None:  
            if not os.path.isfile(self.blastout):  
                logger.critical(f'File <{self.blastout}> does not exist. Please check BLAST output file (--blastout)')  
                sys.exit(2)    
            else:  
                logger.info(f'BLAST output file <{self.blastout}> given, skip BLAST')  
                self.setting.blastout = self.blastout  
        else:  
            # warn if output files already exist  
            if (  
                os.path.isfile(self.setting.blastout) or  
                os.path.isfile(self.setting.extracted_filtered) or  
                os.path.isfile(self.setting.blastout_filtered)  
            ):  
                logger.warning(f'Output folder <{self.outdir}> contains <blastout.txt> and/or <*.filtered.*>, they/it will be overwritten.')

            #remove existing output files
            for file in [self.setting.blastout, self.setting.extracted_filtered, self.setting.blastout_filtered]:  
                try:  
                    os.remove(file)  
                except OSError:  
                    pass  # file does not exist; no action needed
        
        # check if default database exists
        if not os.path.isfile(f'{self.db}.pdb'):
            logger.critical(f'Cannot find database <{self.db}>. Please check database exists')
            sys.exit(2) 
  
    def extract_seqs(self):  
        '''
        Extract target sequences using more stringent cutoffs & blast.
        '''
        logger.info(f'Processing <{self.setting.extracted}> ...')
        nbps, nlines = simple_count(self.setting.extracted)
        mt_mode = '1' if nbps / self.thread >= 2500000 else '0'
        blast_mode = 'blastx'

        logger.info('Extracting target sequences using BLAST ...')
        logger.info(f'BLAST settings: {nbps} bps, {nlines} reads, {self.thread} threads, mt_mode {mt_mode}.')

        subprocess.run([
            blast_mode,
            '-db', self.db,
            '-query', self.setting.extracted,
            '-out', self.setting.blastout,
            '-outfmt', ' '.join(['6'] + self.setting.columns),
            '-evalue', '1e-10',
            '-max_target_seqs', '5',
            '-num_threads', str(self.thread),
            '-mt_mode', mt_mode], check=True)  
  
        # read BLAST output
        df = pd.read_csv(self.setting.blastout, sep='\t', header=None, names=self.setting.columns)  
    
        # filter results based on identity and e-value  
        filtered_df = df[(df['pident'] >= 80) & (df['evalue'] <= 1e-10)]  
  
        # remove duplicates
        filtered_df = filtered_df.sort_values(['qseqid', 'evalue', 'bitscore', 'length'], ascending=[True, True, False, False])  
        filtered_df = filtered_df.drop_duplicates(subset='qseqid', keep='first')  
  
        # save filtered results 
        filtered_df.to_csv(self.setting.blastout_filtered, sep='\t', index=False)  
  
    def split_filtered_results(self):  
    # read filtred BLAST outut
        df = pd.read_csv(self.setting.blastout_filtered, sep='\t', header=0)  
      
    # Extract group key from qseqid (before '@')   
        df['group_key'] = df['qseqid'].apply(lambda x: x.split('@')[0])  
      
    # Group by 'group_key' and save each group to a separate file
        for key, group in df.groupby('group_key'):  
            output_filename = os.path.join(self.outdir, f'{key}.filtered.txt')  
            group.to_csv(output_filename, sep='\t', index=False, header=True)  
      
    def run(self):  
        if self.blastout is None:  
            self.extract_seqs()  
        self.split_filtered_results()
        logger.info('Finished.')  
  
def run_finefilter(options):  
    Finefilter(vars(options)).run()  
