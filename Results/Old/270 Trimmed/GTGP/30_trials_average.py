import os

"""
This script needs to be modified before it is usable.
After you run the model some X number of trials per setting, put all of the trials for each setting in one folder.
Create subfolders for each file type (human demographics, monkey demographics).
Then in each, create an empty .csv that is the same as the set_file_name stated here. This is so it can added to.
Finally, run this script from the same directory as the other .csv files.

This code assumes 3 sets of 30 trials and 1460 steps (20 years). It will take each of the 30 trials' outputs and average them.
The number of trials can be adjusted; the default is 30 ('counter < 31').
"""

set_file_name = 'average_human_population.csv'
import time
def read_first_line(filename, x):
    f = open(filename)
    lines = f.readlines()
    new_file = open(set_file_name, 'a+')
    new_file.writelines(lines[x])
    new_file.close()

def get_values():
    for i in list(range(2, 245)):
        for filename in os.listdir(os.getcwd()):
            if filename[-3:] == 'csv' and str(filename) != str(set_file_name):
                read_first_line(filename, i)  # 0 years

get_values()