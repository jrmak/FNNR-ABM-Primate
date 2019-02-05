import os

def read_first_line(filename):
    f = open(filename)
    lines = f.readlines()
    print(lines[2])

for filename in os.listdir(os.getcwd()):
    if os.path.isfile(filename):
        read_first_line(filename)