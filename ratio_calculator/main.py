# This script is adapted from https://github.com/xinehc/ARGs_OAP
# Original code by Xiaole Yin, licensed under MIT.
# Modifications made to fit the requirements of the BacPosNeg project.

import sys

from argparse import ArgumentParser
from .prefilter import run_prefilter
from .finefilter import run_finefilter
from .ratio_calculator import run_ratio_calculator

#from  import __version__
__version__ = '3.2.4'

## prefilter parameters
def parser_prefilter(parser):
    parser_prefilter = parser.add_parser('prefilter', help='run prefilter pipeline')

    required = parser_prefilter.add_argument_group('required arguments')
    optional = parser_prefilter.add_argument_group('optional arguments')

    required.add_argument(
        '-i',
        '--indir',
        required=True,
        metavar='DIR',
        help='Input folder.')

    required.add_argument(
        '-o',
        '--outdir',
        required=True,
        metavar='DIR',
        help='Output folder.')

    optional.add_argument(
        '-t',
        '--thread',
        metavar='INT',
        default=8,
        type=int,
        help='Number of threads. [8]')

    optional.add_argument(
        '-f',
        '--format',
        metavar='EXT',
        default='fq',
        help='File format in input folder (--indir), gzipped (*.gz) optional. [fq]')

    optional.add_argument(
        '--keep',
        action='store_true',
        help='Keep all temporary files (*.tmp) in output folder (--outdir).')


    parser_prefilter.set_defaults(func=run_prefilter)


## finefilter parameters
def parser_finefilter(parser):
    parser_finefilter = parser.add_parser('finefilter', help='run finefilter pipeline')

    required = parser_finefilter.add_argument_group('required arguments')
    optional = parser_finefilter.add_argument_group('optional arguments')

    required.add_argument(
        '-i',
        '--indir',
        required=True,
        metavar='DIR',
        help='Input folder. Should be the output folder of prefilter (containing <extracted.fa>).')

    optional.add_argument(
        '-t',
        '--thread',
        metavar='INT',
        default=8,
        type=int,
        help='Number of threads. [8]')

    optional.add_argument(
        '-o',
        '--outdir',
        metavar='DIR',
        default=None,
        help='Output folder, if not given then same as input folder (--indir). [None]')

    optional.add_argument(
        '--e',
        metavar='FLOAT',
        default=1e-10,
        type=float,
        help='E-value cutoff for target sequences. [1e-10]')

    optional.add_argument(
        '--id',
        metavar='FLOAT',
        default=80,
        type=float,
        help='Identity cutoff (in percentage) for target sequences. [80]')


    optional.add_argument(
        '--blastout',
        metavar='FILE',
        default=None,
        help='BLAST output (-outfmt "6 qseqid sseqid pident length qlen slen evalue bitscore"), if given then skip BLAST. [None]')


    parser_finefilter.set_defaults(func=run_finefilter)



## ratio_calculator parameters
def parser_ratio_calculator(parser):
    parser_ratio = parser.add_parser('ratio_calculator', help='Calculate the ratio of positive to negative sequences')
    required = parser_ratio.add_argument_group('required arguments')

    required.add_argument(
        '-i',
        '--indir',
        required=True,
        metavar='DIR',
        help='Input directory containing .filtered.txt files.')
    
    required.add_argument(
        '-o',    
        '--outfile',
        required=True,
        metavar='FILE',
        help='Output file to write the ratios.')

    
    parser_ratio.set_defaults(func=run_ratio_calculator)

def main(argv=sys.argv):
    '''entry point'''

    parser = ArgumentParser(description=f'BacPosNegID v{__version__}: online analysis pipeline for the ratio of GP and GN bacteria')
    subparsers = parser.add_subparsers(dest='subcommand', help='descriptions', metavar='{prefilter, finefilter, ratio_calculator}')

    # attach parsers
    parser_prefilter(subparsers)
    parser_finefilter(subparsers)
    parser_ratio_calculator(subparsers)

    # parse arguements
    options = parser.parse_args(argv[1:])

    # print version information
    if ('-v' in argv or '--version' in argv):
        print(__version__)
        return

    # check if a subcommand was selected
    if options.subcommand:
        #call the corresponding function
        options.func(options)
    else:
        # 如果没有选择子命令，打印帮助信息
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)
