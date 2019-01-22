# !/usr/bin/python

import csv
import inspect
import os

"""
Contains three functions: save_summary_humans, save_summary_human_demographics and erase_summary_humans.
erase_summary_humans is currently not being used. Excel files can be erased or deleted manually.
Exports FNNR summary data of human demographics into the Excel files as named below.
"""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-30]  # 'removes excel_export_humans_summary.py' at end
os.chdir(currentpath)  # uses current directory path


def save_summary_humans(run_number, steps, number_of_humans, human_birth_count, human_death_count,
                        human_marriage_count, num_labor, single_male_count, married_male_count, total_migration):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('abm_export_summary_humans' + run_number + '.csv', 'a+')  # w+ resets every time
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    if steps == 6:
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

def save_summary_human_demographics(run_number, steps, male_0, male_1, male_2, male_3, male_4, male_5, male_6,
                                    male_7, male_8, male_9, female_0, female_1, female_2, female_3,
                                    female_4, female_5, female_6, female_7, female_8, female_9):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('abm_export_summary_human_demographics' + run_number + '.csv', 'a+')  # 'w+' resets every time
        # use the string 'a+' setting to append every time instead of reset
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    if steps == 6:
        filewriter = csv.writer(fnnr_export)
        filewriter.writerow(
            ['Steps', 'Male 0-10', 'Male 10-20', 'Male 20-30', 'Male 30-40', 'Male 40-50', 'Male 50-60', 'Male 60-70',
             'Male 70-80', 'Male 80-90', 'Male 90+', 'Female 0-10', 'Female 10-20', 'Female 20-30', 'Female 30-40',
             'Female 40-50', 'Female 50-60', 'Female 60-70', 'Female 70-80', 'Female 80-90', 'Female 90+'
             ])
    fnnr_export.writelines(str(steps))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_0))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_1))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_2))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_3))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_4))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_5))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_6))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_7))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_8))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(male_9))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_0))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_1))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_2))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_3))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_4))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_5))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_6))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_7))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_8))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(female_9))
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
