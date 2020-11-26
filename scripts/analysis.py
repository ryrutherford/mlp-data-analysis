"""
This script will run the analysis on the clean_dialog.csv file and output some metrics about:
    - verbosity,
    - mentions,
    - follow on comments,
    - non-dictionary words
for each of the 5 ponies in MLP
"""

import pandas
import argparse
import os.path as osp
import sys
from compute_metrics import begin_computations

script_dir = osp.normpath(osp.dirname(__file__))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dialog_file", help="the path to clean_dialog.csv")
    parser.add_argument("-o", help="the name of the file to write the json output to",)
    args = parser.parse_args()

    #if you don't want to provide the full path uncomment this line
    #csv_path = osp.join(script_dir, "..", args.dialog_file)

    csv_path = args.dialog_file
    output_location = args.o

    df = pandas.read_csv(csv_path)
    begin_computations(df, output_location)

if __name__ == '__main__':
    main()

