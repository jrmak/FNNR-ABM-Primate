# !/usr/bin/python

import csv
import inspect
import os
from model_for_graph import *

"""
Exports FNNR summary data of monkey demographics into Excel.
"""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-23]  # 'removes excel_export_summary.py' at end
os.chdir(currentpath)


def save_summary(steps, number_of_monkeys, monkey_birth_count, monkey_death_count):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('abm_export_summary.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    if steps == 0:
        filewriter = csv.writer(fnnr_export)
        filewriter.writerow(
            ['Steps', 'Number of Monkeys'])
    fnnr_export.writelines(str(steps))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(number_of_monkeys))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(monkey_birth_count))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(monkey_death_count))
    fnnr_export.writelines('\n')
    fnnr_export.flush()  # flush memory
    fnnr_export.close()

def erase_summary():
    try:
        fnnr_export = open('abm_export_summary.csv', 'w+')  # a+ will create the file if it doesn't exist already
        fnnr_export.truncate()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    fnnr_export.close()