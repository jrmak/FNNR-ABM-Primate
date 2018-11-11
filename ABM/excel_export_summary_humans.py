# !/usr/bin/python

import csv
import inspect
import os

"""
Contains two functions: save_summary_humans and erase_summary_humans.
Exports FNNR summary data of monkey demographics into the Excel file 'abm_export_summary_humans.csv'.
"""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-30]  # 'removes excel_export_humans_summary.py' at end
os.chdir(currentpath)  # uses current directory path


def save_summary_humans(steps, number_of_humans, human_birth_count, human_death_count, human_marriage_count, num_labor,
                 single_male_count, married_male_count, total_migration):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('abm_export_summary_humans.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    if steps == 0:
        filewriter = csv.writer(fnnr_export)
        filewriter.writerow(
            ['Steps', 'Total Humans', 'Births', 'Deaths', 'Marriages', 'Laborers', 'Single Males', 'Married Males',
             'Currently Migrated',
             ])
    fnnr_export.writelines(str(steps))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(number_of_humans))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(human_birth_count))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(human_death_count))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(human_marriage_count))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(num_labor))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(single_male_count))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(married_male_count))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(total_migration))
    fnnr_export.writelines(',')

    fnnr_export.writelines('\n')
    fnnr_export.flush()  # flush memory
    fnnr_export.close()

def erase_human_summary():
    try:
        fnnr_export = open('abm_export_summary_humans.csv', 'w+')  # w+ will create the file if it doesn't exist already
        fnnr_export.truncate()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    fnnr_export.close()
