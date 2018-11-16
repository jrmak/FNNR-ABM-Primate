# !/usr/bin/python
"""
This converts a .csv of only X/Y points to a point shapefile including coordinate counts, using pyshp.
Please install the pyshp library using pip, conda, or your IDE's interpreter tools before running this code.
When the code is run, make sure your imported .csv and exported shapefile are named; change name_of_shp in this code
as well as csvfile = open('this name here.csv', 'r').
"""
import shapefile, csv

name_of_shp = 'shapefile_export1' # change your shapefile name here

csvfile = open('export_density_plot_wo10.csv', 'r')
reader = csv.reader(csvfile, delimiter=',')
csvlist = []
for row in reader:
    csvlist.append(row)
csvstringlist = []
for coord in csvlist:
    csvstringlist.append(str(coord).replace(" ",""))
csvcounts = dict()
for i in csvstringlist:
  csvcounts[i] = csvcounts.get(i, 0) + 1

csvfile.close()
csvfile = open('export_density_plot_wo10.csv', 'r')
reader = csv.reader(csvfile, delimiter=',')
newcsvfile = open('export_density_plot_wo10_new.csv', 'w', newline="")  # newline = "" needed, else space between rows
writer = csv.writer(newcsvfile, delimiter=',')
for row in reader:
    row.append(str(csvcounts[str(row).replace(" ", "")]))
    writer.writerow(row)
# use the following code line to skip the first row if there is a header, though there shouldn't be:
# next(reader, None)
csvfile.close()
newcsvfile.close()
output_shapefile = shapefile.Writer(name_of_shp, shapeType = shapefile.POINT)

# auto-balance means that each point record must have coordinates
output_shapefile.autoBalance = 1
output_shapefile.field('Count','C')
output_shapefile.field('X','F')  # if this was a lat-long float, add ,'8','10' to the end of the parameters
output_shapefile.field('Y','F')
csvfile = open('export_density_plot_wo10_new.csv', 'r')
reader = csv.reader(csvfile, delimiter=',')
for row in reader:
    # create the point geometry
    x = int(row[0])
    y = int(row[1].replace(" ", ""))
    counts = int(row[2])
    output_shapefile.point(x, y)
    output_shapefile.record(x, y, counts)

# When you add this to ArcMap using the 'Add Data' button, you will receive a warning about
# this missing a projection system. That is okay; the x/y of the points are not in lat/long degrees,
# but rather, grid coordinates from the 85 x 100 model grid.