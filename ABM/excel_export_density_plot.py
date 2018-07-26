# !/usr/bin/python

import csv
import inspect
import os

"""
Contains two functions: save_summary and erase_summary.
Exports FNNR summary data of monkey demographics into the Excel file 'abm_export_density_plot.csv'.
"""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-28]  # 'removes excel_export_summary.py' at end
os.chdir(currentpath)  # uses current directory path


def save_density_plot(moved_list, number):
    """Exports entries onto a .csv file"""
    try:
        density_export = open('abm_export_density_plot_wo' + str(number) + '.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    filewriter = csv.writer(density_export)
    filewriter.writerow(['x', 'y'])
    for coordinate in moved_list:
        density_export.writelines(str(str(coordinate[0]) + ', ' + str(coordinate[1])))
        density_export.writelines('\n')
    density_export.flush()  # flush memory
    density_export.close()

def erase_density_plot():
    try:
        density_export = open('abm_export_density_plot.csv', 'w+')  # w+ will create the file if it doesn't exist already
        density_export.truncate()
        density_export.flush()  # flush memory
        density_export.close()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    density_export.close()