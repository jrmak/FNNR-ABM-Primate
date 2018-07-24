"""
text = 'agg_veg60.txt'

out_counter = 0
in_counter = 0
f = open(text, 'r')
body = f.readlines()
abody = body[6:]  # ASCII file with a header
f.close()
with_list = []
for line in abody:
    for item in line.split(" "):
        if str(item) == '-9999':
            out_counter += 1
        else:
            in_counter += 1
print(out_counter, in_counter)
# 3603 coordinates outside FNNR boundaries, 4897 coordinates inside FNNR in 85 x 100 pixel grid
"""

"""
with_humans vs maxent
Kappa Statistic for 1 Count Frequency:
0.697
Kappa Statistic for 5 Count Frequency:
0.578
Kappa Statistic for 10 Count Frequency:
0.391
Kappa Statistic for 15 Count Frequency:
0.272
Kappa Statistic for 20 Count Frequency:
0.078
Kappa Statistic for 50 Count Frequency:
0.0

without vs maxent
Kappa Statistic for 1 Count Frequency:
0.682
Kappa Statistic for 5 Count Frequency:
0.594
Kappa Statistic for 10 Count Frequency:
0.387
Kappa Statistic for 15 Count Frequency:
0.247
Kappa Statistic for 20 Count Frequency:
0.074
Kappa Statistic for 50 Count Frequency:
0.0
"""

text = 'with_maxent.csv'
text = 'without_maxent.csv'

# text = 'with_without_trimmed35.csv'
# text2 = 'with_without_trimmed35_2.csv'


f = open(text, 'r')
body = f.readlines()
abody = body[2:]  # ignore header
f.close()
with_list = []
without_list = []
for line in abody: # format ('57,42,62,73')
    with_list.append(line[:5].strip("\\n"))  # first coordinates of line (first 5 characters, e.g. '57,42')
    without_list.append(str(line[-6:-1]))  # second coordinates of line (last 5 characters, e.g. '62,73')
"""
f2 = open(text2, 'r')
body2 = f2.readlines()
abody2 = body2[2:]  # ASCII file with a header
f2.close()
with_list2 = []
without_list2 = []
for line in abody2:
    with_list2.append(line[:5].strip("\\n"))
    without_list2.append(str(line[-6:-1]))
"""
# could combine the two blocks of code above into one function, no time

full_grid = []

for x in range(85):
    for y in range(66,101):
        full_grid.append(str(x)+ ',' + str(y))

def kappa(with_and_without_count, with_count, without_count, neither_count, frequency_count, possible_grid_count):
    """Calculates Cohen's Kappa Coefficient"""
    p0 = (with_and_without_count + neither_count) / (possible_grid_count)  # 1425 data points in the FNNR, 2975 in 35x85
    pA = with_count / (possible_grid_count)
    pB = without_count / (possible_grid_count)
    pE_presence = pA * pB
    pE_nopresence = (1 - pA) * (1 - pB)
    pE = pE_presence + pE_nopresence
    print('Kappa Statistic for', frequency_count, 'Count Frequency:')
    print(round((p0 - pE)/(1 - pE), 3))  # rounds to 3 decimal places

def calculate_count_x(with_list, without_list, x):
    with_count = 0
    without_count = 0
    with_and_without_count = 0
    with_only_count = 0
    without_only_count = 0
    neither_count = 0
    for coordinate in full_grid:
        if with_list.count(coordinate) >= x:
            with_count += 1
            if without_list.count(coordinate) >= x:
                with_and_without_count += 1
            else:
                with_only_count += 1

        elif without_list.count(coordinate) >= x:
            without_count += 1
            if with_list.count(coordinate) < x:
                without_only_count += 1

        else:
            neither_count += 1

    # print(with_and_without_count, with_count, without_count, neither_count)
    return(with_and_without_count, with_count, without_count, neither_count, x, 2975)

kappa(*calculate_count_x(with_list, without_list, 1))
kappa(*calculate_count_x(with_list, without_list, 5))
kappa(*calculate_count_x(with_list, without_list, 10))
kappa(*calculate_count_x(with_list, without_list, 15))
kappa(*calculate_count_x(with_list, without_list, 20))
kappa(*calculate_count_x(with_list, without_list, 50))
kappa(*calculate_count_x(with_list, without_list, 100))

"""
kappa(*calculate_count_x(with_list, without_list, 1))
kappa(*calculate_count_x(with_list, with_list2, 1))
kappa(*calculate_count_x(without_list, without_list2, 1))
print()
kappa(*calculate_count_x(with_list, without_list, 5))
kappa(*calculate_count_x(with_list, with_list2, 5))
kappa(*calculate_count_x(without_list, without_list2, 5))
print()
kappa(*calculate_count_x(with_list, without_list, 10))
kappa(*calculate_count_x(with_list, with_list2, 10))
kappa(*calculate_count_x(without_list, without_list2, 10))
print()
kappa(*calculate_count_x(with_list, without_list, 15))
kappa(*calculate_count_x(with_list, with_list2, 15))
kappa(*calculate_count_x(without_list, without_list2, 15))
print()
kappa(*calculate_count_x(with_list, without_list, 20))
kappa(*calculate_count_x(with_list, with_list2, 20))
kappa(*calculate_count_x(without_list, without_list2, 20))
print()
kappa(*calculate_count_x(with_list, without_list, 50))
kappa(*calculate_count_x(with_list, with_list2, 50))
kappa(*calculate_count_x(without_list, without_list2, 50))
print()
kappa(*calculate_count_x(with_list, without_list, 100))
kappa(*calculate_count_x(with_list, with_list2, 100))
kappa(*calculate_count_x(without_list, without_list2, 100))
"""
"""
text = 'with_without_trimmed35.csv'
text2 = 'with_without_trimmed35_2.csv'

Kappa Statistic for 1 Count Frequency:
0.813
936 1017 121 1837
Kappa Statistic for 1 Count Frequency:
0.809
1014 1091 95 1789
Kappa Statistic for 1 Count Frequency:
0.846

750 798 132 2045
Kappa Statistic for 5 Count Frequency:
0.79
717 798 89 2088
Kappa Statistic for 5 Count Frequency:
0.797
757 882 78 2015
Kappa Statistic for 5 Count Frequency:
0.778

596 642 129 2204
Kappa Statistic for 10 Count Frequency:
0.755
571 642 60 2273
Kappa Statistic for 10 Count Frequency:
0.806
627 725 61 2189
Kappa Statistic for 10 Count Frequency:
0.79

489 546 107 2322
Kappa Statistic for 15 Count Frequency:
0.733
474 546 58 2371
Kappa Statistic for 15 Count Frequency:
0.777
540 596 64 2315
Kappa Statistic for 15 Count Frequency:
0.811

419 475 84 2416
Kappa Statistic for 20 Count Frequency:
0.737
404 475 43 2457
Kappa Statistic for 20 Count Frequency:
0.774
444 503 69 2403
Kappa Statistic for 20 Count Frequency:
0.767

133 183 33 2759
Kappa Statistic for 50 Count Frequency:
0.608
144 183 46 2746
Kappa Statistic for 50 Count Frequency:
0.619
119 166 32 2777
Kappa Statistic for 50 Count Frequency:
0.594

2 7 4 2964
Kappa Statistic for 100 Count Frequency:
0.18
0 7 5 2963
Kappa Statistic for 100 Count Frequency:
-0.002
0 6 2 2967
Kappa Statistic for 100 Count Frequency:
-0.001
"""