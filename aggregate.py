import pandas as pd
import numpy as np
import os
import helper
import main

# # get clean folder
# data_path = helper.pwd() + '\\test_data'
# output_path_name = main.args.outfile

# # making the dataframe ( CSV that will be exported when done )
# stats = pd.DataFrame({'tag_name': [] , 'tag_epc': [] , 'power': [] , 'number_of_reads': []})
# #epc = main.args.target_epcs

def aggregate(path, output_df):
    # setting variables before use
    epcs = main.args.target_epcs
    print(epcs)
    df = pd.read_csv(path)
    # removing any epc other than our target epc
    for x in epcs:
        if x in df.epc:
            df = df[df.epc == x]
    #print(df)
    # converting power to integer from objects
    df.power = df.power.values.astype(np.int64)
    # preparing values
    name = os.path.split(path)
    name = name[1]
    name = name[:-4]
    # preparing epc
    # df.loc[0,1] = epc
    # getting power levels that are unique
    unique_power_levels = list(df.power.unique())
    # getting reads for each power level
    reads_per_power = df['power'].value_counts()
    reads_per_power = list(reads_per_power)
    print(reads_per_power)
    power = reads_per_power[::-1]
    print(power)
    # loop through each power level and insert the aggregatted data
    print(df)
    for i, x in enumerate(unique_power_levels):
        # this variable gets the number of reads at each unique power level
        num_reads = power[i]
        new_row = {'tag_name': name, 'tag_epc': df['epc'][1], 'power': unique_power_levels[i], 'number_of_reads': num_reads}
        output_df = output_df.append(new_row, ignore_index=True)
    return output_df

def process():
    # get clean folder
    data_path = helper.data_path()
    output_path_name = main.args.outfile

    # making the dataframe ( CSV that will be exported when done )
    stats = pd.DataFrame({'tag_name': [] , 'tag_epc': [] , 'power': [] , 'number_of_reads': []})

    # loop thru directory and aggregate the files
    for entry in os.scandir(data_path):
        if entry.path.endswith('.csv'):
            stats = aggregate(os.path.abspath(entry), stats)

    stats.to_csv('OUT.csv', index=False)

def main():
    process()

if __name__ == '__main__':
    main()