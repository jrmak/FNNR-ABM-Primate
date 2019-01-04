# !/usr/bin/python
import csv
import inspect
import os

"""
Contains two functions: save_summary and erase_summary.
Exports FNNR movement data into the Excel file 'abm_export_density_plot.csv'.
"""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-28]  # 'removes excel_export_summary.py' at end
os.chdir(currentpath)  # uses current directory path


def save_density_plot(moved_list, number):
    """Exports entries onto a .csv file"""
    try:
        density_export = open('abm_export_density_plot' '.csv', 'w+')
        # density_export = open('export_density_plot_' + str(number) + '.csv', 'w+')
        # the + will create the file if it doesn't exist already
        # change the name of this file manually each run if changing testing styles to collect new data
        # without overwriting, e.g. naming the file with '_wo#.csv' vs '_w#.csv' for without or with humans
        # the str(number) is movement_session_id in graph.py - edit this after each run
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
        density_export = open('abm_export_density_plot.csv', 'w+')  # w+ will create the file if it doesn't exist already
        density_export.truncate()
        density_export.flush()  # flush memory
        density_export.close()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    density_export.close()
