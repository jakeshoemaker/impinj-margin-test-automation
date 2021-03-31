import pandas as pd
import numpy as np
import argparse
import helper
import aggregate
import shutil
import send2trash
import os

"""

refactor and change the output directory to watch a folder.
    - the csv file is going to have the power at the end of each run, therefore I would need to append it to each run.
    - another suggestion is getting reads per powerlevel because we know how long the margin test was ran ( assumed 5 seconds )
    
"""

# if no path is set, then use the users download file
download_path = helper.get_download_path()

parser = argparse.ArgumentParser(description='itemtest data cleaner, parses the files and combines the data into one file for easy analysis')
parser.add_argument('--path', type=str, help='path of the csv folders', default=helper.data_path())
parser.add_argument('--target_epcs', type=list, default=['0000 4353 5744 5344 FFF0 002C'], help='The tag you ran testing on, if no tag specified, then all tags will be show on report', required=False)
parser.add_argument('--outfile', type=str, default='out.csv')
parser.add_argument('--tag-names', type=str, default='default')
parser.add_argument('--test', type=bool, default=True)

args = parser.parse_args()
print(args)

# power is the last item in row therefore:
#   power = data[-1]

def main():
    tag_list = get_tag_names(args.tag_names)
    path = args.path

    # looping through the folders to merge into concise files
    for entry in os.scandir(path):
        # check to loop through the files
        csv_list = []
        if entry.is_dir():
            subdir = entry
            for entry in os.scandir(subdir):
                if entry.path.endswith('.csv'):
                    csv = perform_operations_on_csv(entry.path)
                    # removing bad data, and filling it with the correct labels
                    csv_list.append(csv)
        elif entry.path.endswith('.csv'):
            csv = perform_operations_on_csv(entry.path)
            # send to merge function to merge into one big file
            csv_list.append(csv)
            subdir = path

    merge(csv_list, subdir)
    #aggregate.process()



def perform_operations_on_csv(file_name):
    # editing for csv format that is current
    #prepend_line(file_name)
    dbm = get_power_level(file_name)
    #remove_lines(file_name)
    #print('power = ' + str(dbm))
    csv = pd.read_csv(file_name)
    csv.power.fillna(dbm, inplace = True)
    csv.fillna('0', inplace = True)
    # appending corrected data frame to csv list to merge csv's
    return csv

                    
                   
def get_tag_names(tag_names):
    return tag_names.split()


def prepend_line(file_name):
    first_line = "timestamp,epc,antenna,rssi,frequency,hostname,phaseAngle,dopplerFrequency,power"
    dummy_file = file_name + '.bak'

    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        if read_obj.readline() == first_line:
            print('labels already created')
        else:
            # Write given line to the dummy file
            write_obj.write(first_line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # removing dummy file and rewriting the original name
    os.remove(file_name)
    os.rename(dummy_file, file_name)


def get_power_level(csv):
    #phrase = 'PowerInDbm='
    power = ''
    with open(csv, 'r') as csv:
        for line in csv.readlines():
            power = line
            # if phrase in line:
                # power = line[115:117]
                # print('\nPower level in DbM: ' + power)
    
    return int(power)
    

def remove_lines(csv):
    with open(csv, "r") as f:
        lines = f.readlines()
    with open(csv, "w") as f:
        for line in lines:
            if line[0:2] != "//":
                f.write(line)
    #print('\ncsv files ready to be put into dataframes\n')


def merge(csvs, name):
    out_name = name.path + '.csv'
    
    for csv in csvs:
        if csv.empty == True:
            del csv

    summary = pd.concat(csvs)  
    # write files to one big csv
    pd.DataFrame.to_csv(summary, out_name, sep=',', na_rep='.', index=False)
    



if __name__=='__main__':
    if args.test:
         # removing the used data and replacing it with fresh data to use.
        send2trash.send2trash('C:\\Users\\jshoemaker\\Desktop\\tagtest_tool\\test_data')
        shutil.copytree('C:\\Users\\jshoemaker\\Desktop\\tagtest',
            'C:\\Users\\jshoemaker\\Desktop\\tagtest_tool\\test_data')
        main()

    else:
        main()

    