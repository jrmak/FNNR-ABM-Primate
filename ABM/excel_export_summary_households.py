# !/usr/bin/python

import csv
import inspect
import os

"""
Contains two functions: save_summary_household and erase_summary_household.
Exports FNNR summary data of land/GTGP/income changes into the Excel file 'export_summary_household.csv'.
Appends each run.
"""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-34]  # 'removes excel_export_household_summary.py' at end
os.chdir(currentpath)  # uses current directory path


def save_summary_households(run_number, steps, total_non_gtgp, total_gtgp, average_non_gtgp_per_hh,
                            average_gtgp_per_hh, average_non_gtgp_land_area_per_hh, average_gtgp_land_area_per_hh,
                            scenario, household_area, farm_area, forest_area
                            ):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('abm_export_summary_household' + '_'
                            + household_area + '_' + farm_area + '_' + forest_area + '_' + run_number + '.csv', 'a+')
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