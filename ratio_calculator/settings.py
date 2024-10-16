# This script is adapted from https://github.com/xinehc/ARGs_OAP
# Original code by Xiaole Yin, licensed under MIT.
# Modifications made to fit the requirements of the BacPosNeg project.

import os
import re
import logging

from dataclasses import dataclass

## setup logger
logging.basicConfig(
    level="INFO",
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

## bold format
BOLD = "\033[1m"
RESET = "\033[0m"

## add color
logging.addLevelName(
    logging.WARNING,
    BOLD + "\x1b[33;20m%s\033[1;0m" % logging.getLevelName(logging.WARNING))

logging.addLevelName(
    logging.CRITICAL,
    BOLD + "\x1b[31;20m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))

logger = logging.getLogger(__name__)

## setup file format
@dataclass
class File:
    file: str
    outdir: str
    format: str

    @property
    def file_name(self) -> str:
        return re.sub(rf'\.{self.format}(.gz)?$', '', os.path.basename(self.file))

    @property
    def sample_name(self) -> str:
        return re.sub(r'(_R1|_R2|_1|_2|_fwd|_rev)$', '', self.file_name)

    @property
    def tmp_seqs_fa(self) -> str:
        return os.path.join(self.outdir, self.file_name + '.seqs.fa.tmp')

    @property
    def tmp_seqs_txt(self) -> str:
        return os.path.join(self.outdir, self.file_name + '.seqs.txt.tmp')

    @property
    def tmp_seqs_sam(self) -> str:
        return os.path.join(self.outdir, self.file_name + '.seqs.sam.tmp')


## setup database
@dataclass
class Setting:
    indir: str
    outdir: str
    db: str = os.path.join(os.path.dirname(__file__), 'db')

    @property
    def nps(self) -> str:
        return os.path.join(self.db, 'GramPN')


    @property
    def extracted(self) -> str:
        if self.indir is None:
            return os.path.join(self.outdir, 'extracted.fa')
        else:
            return os.path.join(self.indir, 'extracted.fa')

    @property
    def blastout(self) -> str:
        return os.path.join(self.outdir, 'blastout.txt')

    @property
    def blastout_filtered(self) -> str:
        return os.path.join(self.outdir, 'blastout.filtered.txt')

    @property
    def extracted_filtered(self) -> str:
        return os.path.join(self.outdir, 'extracted.filtered.fa')

    @property
    def columns(self) -> list:
        return ['qseqid', 'sseqid', 'pident', 'length', 'qlen', 'slen', 'evalue', 'bitscore']
