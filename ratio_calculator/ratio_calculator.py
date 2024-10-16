import os  
import pandas as pd  
  
class Ratio_Calculator:  
    def __init__(self, indir, outfile):  
        self.indir = indir  
        self.outfile = outfile    
  
    def calculate_ratios(self):  
        # get all .filtered.txt files in the directory 
        filtered_files = [f for f in os.listdir(self.indir) if f.endswith('.filtered.txt') and f != 'blastout.filtered.txt']  
        results = []  
  
        # process each .filtered.txt file
        for filename in filtered_files:  
            filepath = os.path.join(self.indir, filename)    
            try:  
                df = pd.read_csv(filepath, sep='\t', header=0)  
            except (FileNotFoundError, pd.errors.EmptyDataError) as e:  
                print(f"Warning: Could not read file {filename}. Skipping: {e}")  
                continue  
  
            #  keep the entry with the highest bitscore for each qseqid
            df_sorted = df.sort_values(by=['qseqid', 'bitscore'], ascending=[True, False])  
            df_unique = df_sorted.drop_duplicates(subset='qseqid', keep='first')  
  
            # calculate the 'count' for each sseqid
            df_unique['count'] = df_unique['length'] / (3 * df_unique['slen'])  
        
            grouped = df_unique.groupby('sseqid')['count'].sum()  
  
            # sum the counts for sseqids starting with 'n_' and 'p_'  
            negative_sum = grouped[grouped.index.str.startswith('n_')].sum()  
            positive_sum = grouped[grouped.index.str.startswith('p_')].sum()  
  
            # calculate the ratio
            ratio = (10.042586 * (positive_sum / negative_sum)) if negative_sum > 0 else float('inf')  
  
            # add the results to the list  
            sample_name = filename.split('.filtered.txt')[0]  
            results.append((sample_name, positive_sum, negative_sum, ratio))  
  
        # write all results to the output file
        self.write_results(results)

    def write_results(self, results):  
        # write SampleName, TotalPositive, TotalNegative, and Ratio to the output file  
        with open(self.outfile, 'w') as f:  
            f.write('SampleName\tTotalPositive\tTotalNegative\tRatio\n')  
            for sample_name, total_positive, total_negative, ratio in results:  
                f.write(f'{sample_name}\t{total_positive:.2f}\t{total_negative:.2f}\t{ratio:.2f}\n')  
  
def run_ratio_calculator(options):  
    indir = getattr(options, 'indir', None)  
    outfile = getattr(options, 'outfile', None)  
    if indir and outfile:  
        ratio_calc = Ratio_Calculator(indir, outfile)  
        ratio_calc.calculate_ratios()  
    else:  
        print("Error: Both 'indir' and 'outfile' are required.")  
