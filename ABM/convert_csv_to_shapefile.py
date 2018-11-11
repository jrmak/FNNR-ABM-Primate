# !/usr/bin/python
"""
This converts a .csv of only headers and points to a point shapefile using pyshp.
Please install the pyshp library using pip, conda, or your IDE's interpreter tools before running this code.
When the code is run, make sure your imported .csv and exported shapefile are named (change in this code).
"""
import shapefile, csv

name_of_shp = 'shapefile_export1' # change your shapefile name here

output_shapefile = shapefile.Writer(name_of_shp, shapeType = shapefile.POINT)

# auto-balance means that each point record must have coordinates
output_shapefile.autoBalance = 1
csvfile = open('export_density_plot_wo10.csv', 'r')
reader = csv.reader(csvfile, delimiter=',')
# use the following code line to skip the first row if there is a header, though there shouldn't be:
# next(reader, None)
output_shapefile.field('X','F')  # add 10, 8 to parameters if float; not done here because x/y are grid coords
output_shapefile.field('Y','F')
for row in reader:
    # create the point geometry
    x = row[0]
    y = row[1]
    output_shapefile.point(int(x.replace(" ","")),int(y.replace(" ","")))

# When you add this to ArcMap using the 'Add Data' button, you will receive a warning about
# this missing a projection system. That is okay; the x/y of the points are not in lat/long degrees,
# but rather, grid coordinates from the 85 x 100 model grid.