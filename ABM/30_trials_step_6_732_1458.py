import os

"""
This script needs to be modified before it is usable.
After you run the model some X number of trials per setting, put all of the trials for each setting in one folder.
Create subfolders for each file type (human demographics, monkey demographics).
Finally, run this script from the same directory as the other .csv files.

This code assumes 3 sets of 30 trials and 1460 steps (20 years). It will take each of the 30 trials' outputs for each setting.
Then it writes the output for steps 6 (0 years), 732 (10 years), and 1458 (20 years).
After this, averages for 30 trials can be generated for each time frame, which will make for more accurate graphs/plots.
Repeat this code for each setting, then again for each type of output file (human demographics, monkey demographics, etc.).
"""

set_file_name = 'GTGP_270.csv'

def read_first_line(filename, x):
    if filename[-3:] == 'csv' and filename is not set_file_name:
        f = open(filename)
        lines = f.readlines()
        new_file = open(set_file_name, 'a+')
        new_file.writelines(lines[x])
        new_file.close()

counter = 0
for filename in os.listdir(os.getcwd()):
    if os.path.isfile(filename) and counter < 31:
        read_first_line(filename, 2)  # 0 years
        counter += 1
counter = 0
for filename in os.listdir(os.getcwd()):
    if os.path.isfile(filename) and counter < 31:
        read_first_line(filename, 123)  # 10 years
        counter += 1
counter = 0
for filename in os.listdir(os.getcwd()):
    if os.path.isfile(filename) and counter < 31:
        read_first_line(filename, 244)  # 20 years
        counter += 1
