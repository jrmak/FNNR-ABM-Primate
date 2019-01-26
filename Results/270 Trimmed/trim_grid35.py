#!/usr/bin/python

"""
Deletes coordinates from a csv file if its y value is below 65 (for an 85x100 spatial grid,
this creates an 85x35 segment of the top portion).
"""


#text = 'testing.csv'
def readCSV(file, number):
    f = open(file + str(number) + '.csv', 'r+')
    body = f.readlines()
    abody = body[2:]  # ignore header
    f.seek(0) # reset pointer
    for line in abody: # format ('57,42,62,73')
        if len(line) == 7:
            if int(line[4:6]) >= 65:
                f.write(line)
        else:
            if len(line.split(",")[0]) == 1 and line.split(",")[0] != 'x' and \
                    line.split(",")[0] != '\n' and int(line.split(",")[0]) < 11 :
                if int(line[3:5]) >= 65:
                    f.write(line)
    f.truncate()
    f.close()

for numb in range(1,31):
    text = 'abm_export_density_plot_with_humans_'
    print('Progress: ' + str(numb) + ' / 30')
    readCSV(text, numb)
