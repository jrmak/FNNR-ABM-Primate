import os
import time

"""
This script takes model file outputs and creates an 'average' run out of those files, for use in creating a summary Excel graph
for scientific purposes. For educational or observational purposes, you can skip straight to creating an Excel graph from any single
model run's file output; this script is optional.

After you run the model some X number of trials per setting, put all of the trials for each setting in one folder.
Create subfolders for each file type (all human demographic output files in one folder, etc.).
Then run this script from the same directory as the other .csv files.

This code assumes 3 sets of 30 trials and 1460 steps (20 years). It will take each of the 30 trials' outputs and average them.
In other words, the output of this script looks like a new model run, but its step values are just the average of the input files' values.
The number of rows should be adjusted from 245 to however many that your output files have. 245 is the default for a 20-year model run.
"""

set_file_name = 'average_human_population.csv'
with open(set_file_name, 'a+') as f:  # create the file if it doesn't exist yet
    f.close()

def read_first_line(filename, x):  # x refers to i below and represents the step number in the model
    f = open(filename)
    lines = f.readlines()
    new_file = open(set_file_name, 'a+')
    new_file.writelines(lines[x])
    new_file.close()

def get_values():
    for i in list(range(2, 245)):  # the range goes to 245 to include all rows, aka all 1460 time-steps in a 20-year script run
        for filename in os.listdir(os.getcwd()): 
            # os.getcwd() is the current directory as a string
            # os.listdir(directory_name) lists the files in directory_name
            if filename[-3:] == 'csv' and str(filename) != str(set_file_name):  # excludes already-created file if script runs twice
                read_first_line(filename, i)
get_values()
