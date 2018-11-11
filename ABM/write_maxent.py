import csv
import inspect
import os

text = 'maxent_agg_translated_35.csv'


f = open(text, 'r')
body = f.readlines()
abody = body[6:]
f.close()
grid = []
numbers = []
for line in abody:
    grid.append(line.strip("\\n").split(","))
for line in grid:
    for x in line:
        if x != 'NA' and x != '' and x != 'NA\n':
            numbers.append(float(x))

# print(grid[2][53].strip("NA").strip(","))
currentpath = str(inspect.getfile(inspect.currentframe()))[:-20]  # 'removes excel_export_summary.py' at end
os.chdir(currentpath)  # uses current directory path

try:
    max_refresh = open('maxent.csv', 'w+')  # w+ will create the file if it doesn't exist already
    max_refresh.truncate()
    max_refresh.close()
except IOError:
    print('Please close Excel and retry.')  # will not work if the .csv is already open

try:
    maxent = open('maxent.csv', 'a+')  # a+ will create the file if it doesn't exist already
except IOError:
    print('Please close Excel and retry.')  # will not work if the .csv is already open

for y in range(35):
    for x in range(85):
        for number in numbers:
            try:
                if float(grid[y][x].strip("NA").strip(",")) == number:
                    if 0.092744 > number:
                        pass
                    elif 0.092744 < number < 0.185489:  # 10th percentile of value (not count), frequency 1
                        maxent.writelines(str(100 - y) + ',' + str(x + 1))
                        maxent.writelines('\n')
                    elif 0.185489 < number < 0.278261:  # 20th percentile of value (not count), frequency 5
                        for i in range(2):
                            maxent.writelines(str(100 - y) + ',' + str(x + 1))
                            maxent.writelines('\n')
                    elif 0.278261 < number < 0.463722:  # 30th percentile of value (not count), , frequency 10
                        for i in range(5):
                            maxent.writelines(str(100 - y) + ',' + str(x + 1))
                            maxent.writelines('\n')
                    elif 0.463722 < number < 0.649211:  # 50th percentile of value (not count), frequency 15
                        for i in range(10):
                            maxent.writelines(str(100 - y) + ',' + str(x + 1))
                            maxent.writelines('\n')
                    elif 0.649211 < number < 0.8347:  # 70th percentile of value (not count), frequency 20
                        for i in range(15):
                            maxent.writelines(str(100 - y) + ',' + str(x + 1))
                            maxent.writelines('\n')
                    elif 0.8347 < number < 1:  # 90th percentile of value (not count), frequency 50
                        for i in range(20):
                            maxent.writelines(str(100 - y) + ',' + str(x + 1))
                            maxent.writelines('\n')
            except ValueError: # if not float, ignore
                pass
maxent.flush()  # flush memory
maxent.close()

"""
print(grid[2][54].strip("NA").strip(","))
98, 54 0.06125
"""
