import os

def read_first_line(filename, x):
    if filename[-3:] == 'csv' and filename is not 'demo_540.csv':
        f = open(filename)
        lines = f.readlines()
        new_file = open('demo_540.csv', 'a+')
        new_file.writelines(lines[x])
        new_file.close()

counter = 0
for filename in os.listdir(os.getcwd()):
    if os.path.isfile(filename) and counter < 31:
        read_first_line(filename, 2)  # 0 years
        counter += 1
counter = 0
for filename in os.listdir(os.getcwd()):
    if os.path.isfile(filename) and counter < 31:
        read_first_line(filename, 123)  # 10 years
        counter += 1
counter = 0
for filename in os.listdir(os.getcwd()):
    if os.path.isfile(filename) and counter < 31:
        read_first_line(filename, 244)  # 20 years
        counter += 1


