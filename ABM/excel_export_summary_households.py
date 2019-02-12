# !/usr/bin/python

import csv
import inspect
import os
from fnnr_config_file import scenario, unit_comp_flat, \
    unit_comp_dry, unit_comp_rice, unit_comp_before, unit_comp_after, time_breakpoint

"""
Contains two functions: save_summary_household and erase_summary_household.
Exports FNNR summary data of land/GTGP/income changes into the Excel file 'export_summary_household.csv'.
Appends each run.
"""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-34]  # 'removes excel_export_household_summary.py' at end
os.chdir(currentpath)  # uses current directory path


def save_summary_households(run_number, steps, total_non_gtgp, total_gtgp, average_non_gtgp_per_hh,
                            average_gtgp_per_hh, average_non_gtgp_land_area_per_hh, average_gtgp_land_area_per_hh
                            ):
    """Exports entries onto a .csv file"""
    try:
        if scenario.lower() == 'flat':
            fnnr_export = open('abm_export_summary_household' + '_' + scenario + '_'
                               + str(unit_comp_flat) + '_' + run_number + '.csv', 'a+')
        elif scenario.lower() == 'land_type':
            fnnr_export = open('abm_export_summary_household' + '_' + scenario + '_'
                               + str(unit_comp_dry) + 'd' + '_' + str(unit_comp_rice) + 'r'
                               + '_' + run_number + '.csv', 'a+')
        elif scenario.lower() == 'time':
            fnnr_export = open('abm_export_summary_household' + '_' + scenario + '_'
                               + str(unit_comp_before) + '_' + str(time_breakpoint)
                               + '_' + str(unit_comp_after) + '_' + run_number + '.csv', 'a+')
        # a+ will create the file if it doesn't exist
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    if steps == 6:
        filewriter = csv.writer(fnnr_export)
        filewriter.writerow(
            ['Steps', 'Total # Non-GTGP Parcels', 'Total # GTGP Parcels',
             'Avg # Non-GTGP Parcels', 'Avg GTGP Parcels', 'Avg Non-GTGP Area',
             'Avg GTGP Area'
             ])
    fnnr_export.writelines(str(steps))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(total_non_gtgp))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(total_gtgp))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(average_non_gtgp_per_hh))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(average_gtgp_per_hh))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(average_non_gtgp_land_area_per_hh))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(average_gtgp_land_area_per_hh))
    fnnr_export.writelines(',')
    #nnr_export.writelines(str(average_hh_income))
    #fnnr_export.writelines(',')
    fnnr_export.writelines('\n')
    fnnr_export.flush()  # flush memory
    fnnr_export.close()

def erase_household_summary():
    try:
        fnnr_export = open('abm_export_summary_household.csv', 'w+')  # w+ will create the file if it doesn't exist already
        fnnr_export.truncate()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    fnnr_export.close()
