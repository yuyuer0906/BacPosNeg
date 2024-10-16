# BacPosNeg

This repository was created by Yuyu Shi (_yuyuer0906_). It is a bioinformatics tool that provides two primary functionalities:

1.**Genome Classification**: Classifies genomes into Gram-positive (GP) or Gram-negative (GN) bacteria using machine learning models.

2.**GP/GN Ratio Calculation**: Calculates the ratio of GP/GN bacteria in metagenomic datasets.

This repository is designed to simplify the process of analyzing genomic data by automating both classification and ratio calculation steps. The tool is built on Python and leverages DIAMOND and BLAST for pre-filtering and fine-filtering genomic data.

If you have any questions, please create an issue, or contact Yuyu Shi ([shiyuyu1978@outlook.com](shiyuyu1978@outlook.com)).

## Installation

### Prerequisites

- Python 3.7+
- Required dependencies (listed in `requirements.txt`)
- `diamond>=2.0.15`, `blast>=2.12`, `samtools>=1.15`, `prodigal>=2.6.3`, `hmmsearch>=3.4`

### Step 1: Clone the Repository

```bash
git clone https://github.com/yuyuer0906/BacPosNeg.git
cd BacPosNeg
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Realted Tools

You can manually install `Diamond`, `Blast`, `Samtools`, `Prodigal`, `Hmmsearch` from their respective sources:

- [Diamond](https://github.com/bbuchfink/diamond)
- [Blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)
- [Samtools](https://github.com/samtools/samtools)
- [Prodigal](https://github.com/hyattpd/Prodigal)
- [Hmmsearch](https://github.com/EddyRivasLab/hmmer)

### Step 4: Download and Add the `markers.hmm` File

Due to the large size of the `markers.hmm` file, it is NOT included in this repository. You need to download it from the following link and unzip it into the genome_classifier/data directory.

```bash
wget -O markers.hmm.gz "https://drive.google.com/uc?export=download&id=1bCihiTMvaKkwNx6lUzpvtfmxAwVn__ja"
gunzip markers.hmm.gz
mv markers.hmm genome_classifier/data/
```

**NOTE: Manual Download Option**: 

If the `wget` command fails to download the file, you can manually download it by clicking [here](https://drive.google.com/uc?export=download&id=1bCihiTMvaKkwNx6lUzpvtfmxAwVn__ja). After downloading, unzip and place the `markers.hmm` in the `genome_classifier/data/` directory manually.
 
### Step 5: Install BacPosNeg Locally

```bash
pip install -e .
```

## Usage

### Genome Classification: 

1.
Preparing a `completeness.csv`

`CheckM2` and `Quast` are recommended to assess the completeness of genomes, you can manually run `CheckM2` or `Quast` from their respective usage instructions:

- [CheckM2](https://github.com/chklovski/CheckM2)
- [Quast](https://github.com/ablab/quast)

After running `CheckM2` or `Quast`, please extract the relevant completeness informationthe from each genome's report and manually create or automate the creation of `completeness.csv` in the following format:

```bash
Genome,Completeness
Genome1,45
Genome2,21
```

2.
```bash
genome_classifier -i /path/to/genome_data -o /path/to/output_dir -c /path/to/completeness_file.csv -t 180
```

`-i`: Input directory containing genome files (.fna/.fasta/.fa format).

`-o`: Output directory where results will be saved.

`-c`: `CSV` file containing genome completeness data (required to select between Decision Tree or XGBoost).

`-t`: Threads of CPU.

### GP/GN Ratio Calculation:

### Usage 

```bash
ratio_calculator prefilter -i /path/to/metagenomic_reads -o /path/to/output_dir -f fa/fq -t 180
ratio_calculato finefilter -i /path/to/output_dir -o /path/to/output_dir -t 180
ratio_calculator ratio_calculator -i /path/to/output_dir -o /path/to/output_dir/ratio
```

`-i`: Input directory containing metagenomic reads (.fa/.fa.gz or .fq/.fq.gz format). If you use paired-end files, please make sure the forward/reverse reads end with `_1|_2`,` _R1|_R2` or `_fwd|_rev` before the file extension, for example, `test_1.fa and test_2.fa`.

`-o`: Output directory where results will be saved.

`-t`: Threads of CPU.

`-f`: Format of input file.

### Example

We have provided example data for users to test both genome classification and GP/GN bacteria ratio calculation. You can find them in `genome_classifier/example` directory and `ratio_calculator/sample` dierctory.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

This repository uses code and sample data in `GP/GN Ratio Calculation` from the following sources:

- **[ARGs_OAP]**: [args_oap](https://github.com/xinehc/ARGs_OAP). The code and data are licensed under the MIT.

We are grateful to the authors for sharing their work.

## Citation

- Xiaole Yin, ..., Tong Zhang, ARGs-OAP v3.0: Antibiotic resistance gene database curation and analysis pipeline optimization, Engineering, 2023.




