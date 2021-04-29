#!/usr/bin/env python3

import os
import sys
import pandas as pd
from features import *

USAGE = f"Usage: python {sys.argv[0]} [--help | -h] | [<preprocessed dataset.csv filename> <new dataset label>]"

def main():

    #---------------------------------------------------#
    #   Read command line arguments                     #
    #---------------------------------------------------#

    if len(sys.argv) == 3:
        if sys.argv[1] in os.listdir():
            script, file, dataset_label = sys.argv
            dataset_label = '_' + dataset_label
            filename = file[:-4]
        else:
            print('Dataset import error')
            raise SystemExit(USAGE)

    elif len(sys.argv) == 2:
        script = sys.argv[0]

        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print(f'''
            {USAGE}

            TO WRITE: HELP

            An optional second argument can be used to keep multiple outputs separated.
            Not specifying a label can lead to overwriting files.

            e.g. python {script} dataset.csv v1
            ''')
            sys.exit()

        if sys.argv[1] in os.listdir():
            file = sys.argv[1]
            filename = file[:-4]
            dataset_label = ''
        else:
            print('Dataset import error')
            raise SystemExit(USAGE)

    #---------------------------------------------------#
    #   Open dataset and generate dataframe to store    #
    #   the extracted features.                         #
    #---------------------------------------------------#

    df = pd.read_csv(file, sep = ',')

    # Add column with the text number for its use in the feature extraction functions

    df['text_n'] = df.index

    # Add feature columns and fill them with empty values
    for index in indices:
        df[index] = np.nan


    for index in indices:
        apply_index_getter(df, index, level = 'doc')


    df.to_csv(f'vectorized_{filename}{dataset_label}.doc.csv', sep = ',')

    for index in indices:
        apply_index_getter(df, index, level = 'sen')

    df.to_csv(f'vectorized_{filename}{dataset_label}.sen.csv', sep = ',')

if __name__ == "__main__":
   main()
