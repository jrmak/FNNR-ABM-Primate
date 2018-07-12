# !/usr/bin/python

import csv
import inspect
import os

"""
Contains two functions: save_summary and erase_summary.
Exports FNNR summary data of monkey demographics into the Excel file 'abm_export_summary.csv'.
"""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-23]  # 'removes excel_export_summary.py' at end
os.chdir(currentpath)  # uses current directory path


def save_summary(steps, number_of_monkeys, monkey_birth_count, monkey_death_count, demographic_structure_list,
                 female_list, male_maingroup_list, reproductive_female_list):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('abm_export_summary.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    if steps == 0:
        filewriter = csv.writer(fnnr_export)
        filewriter.writerow(
            ['Steps', 'Total Monkeys', 'Births', 'Deaths', 'Age 0-1', 'Age 1-3', 'Age 3-7',
             'Age 7-10', 'Age 10-25', 'Pop Age 25+', 'F:M Ratio', 'Rep. Female'])
    fnnr_export.writelines(str(steps))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(number_of_monkeys))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(monkey_birth_count))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(monkey_death_count))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(demographic_structure_list[0]))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(demographic_structure_list[1]))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(demographic_structure_list[2]))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(demographic_structure_list[3]))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(demographic_structure_list[4]))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(demographic_structure_list[5]))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(len(female_list)/len(male_maingroup_list)) + ':1')
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(len(reproductive_female_list)))
    fnnr_export.writelines(',')
    fnnr_export.writelines('\n')
    fnnr_export.flush()  # flush memory
    fnnr_export.close()

def erase_summary():
    try:
        fnnr_export = open('abm_export_summary.csv', 'w+')  # w+ will create the file if it doesn't exist already
        fnnr_export.truncate()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    fnnr_export.close()