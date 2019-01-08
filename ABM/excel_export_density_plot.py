# !/usr/bin/python
import csv
import inspect
import os
from fnnr_config_file import human_setting

"""
Contains two functions: save_summary and erase_summary.
Exports FNNR movement data into the Excel file 'abm_export_density_plot.csv'.
"""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-28]  # 'removes excel_export_summary.py' at end
os.chdir(currentpath)  # uses current directory path


def save_density_plot(moved_list, number):
    """Exports entries onto a .csv file"""
    try:
        density_export = open('abm_export_density_plot_' + human_setting + '_' + str(number) + '.csv', 'w+')
        # a+ will create the file if it doesn't exist already
        # change the name of this file manually each run if changing testing styles to collect new data
        # without overwriting, e.g. naming the file with 'wo' vs 'w' for without or with humans
        # a is also preferred to w here at the end to append, rather than overwrite, values
        # the str(number) is movement_session_id in graph.py
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    filewriter = csv.writer(density_export)
    for coordinate in moved_list:
        density_export.writelines(str(str(coordinate[0]) + ', ' + str(coordinate[1])))
        density_export.writelines('\n')
    density_export.flush()  # flush memory
    density_export.close()

def erase_density_plot():
    try:
        density_export = open('abm_export_density_plot_with_humans_replacethiswith#.csv', 'w+')  # write in your own file
        density_export.flush()  # flush memory
        density_export.close()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    density_export.close()
