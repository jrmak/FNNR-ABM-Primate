# FNNR-ABM-Primate

Welcome! This project seeks to understand population demographics and factors affecting the movement of Guizhou golden monkeys endemic to the Fanjingshan National Nature Reserve in Guizhou, China.
It uses Mesa, a library framework with tools designed to support agent-based modeling in Python 3.X.
EDIT: This model has been expanded since August and October; the information in the User's Manual and this readme is now outdated and will be updated in February.

An overview of Mesa can be found at: https://mesa.readthedocs.io/en/master/overview.html
A more thorough doc can be found at: https://media.readthedocs.org/pdf/mesa/latest/mesa.pdf

Documentation for this project--as well as the source code available for download--can be found here. Please refer to the User's Manual.

Instructions for Running the Code:
1. Have Python 3.X installed, as well as the Mesa (which comes with dependencies such as numpy, pandas, and tornado) and matplotlib libraries.

!IMPORTANT!
*If you have errors running the code, make sure Mesa's edition is 0.8.3, and tornado's edition is 4.5.2.*

2. Download the code. Files are found in the ABM folder, though the Data folder has some files that are used for processing the data, using Microsoft Excel for some parts. Please refer to the later sections of the User's Manual, found in the parent directory of this repository, for more information.

3a. Edit settings in 'fnnr_config_file.py' (optional) and run 'server.py' to launch a web browser with an interactive visualization module of monkey movement and human resource gathering.
Monkey movements are semi-randomized, and based on the weighted value of their 8-neighbor surroundings.
This weighted value is currently determined by vegetation, human presence, season, and elevation (changeable in code; requires raster layers converted to an ASCII file).
Human movement during resource gathering will be recorded in the data, but shown only as a flicker between resource sites.
A web app version of server.py is being worked on.

3b. Edit settings in 'fnnr_config_file.py' (optional) and run 'graph.py' to see population demographic charts after 10 years, or 730 time-steps (changeable in code). graph.py also provides all data output (Excel file export)--graph.py is the main file to run for data analysis; server.py is simply a demonstration.

4. Once the model is run, 'run trim_grid35.py' on the 'abm_export_density_plot_with_humans_1.csv' file, then 'convert_csv_to_shapefile.py' on the trimmed version (rename the output shapefile within the code if you wish). Open the shapefile in ArcMap by using 'Add Data', select 'Zoom to Layer' from right-clicking the layer, and symbolize the layer with graduated colors. (While selecting the break type, you can also increase the sample size of the layer to 300,000 to avoid the warning.) The other results are freely available to analyze with Excel; some tools, such as 'kappa_batch.py', have been developed, but need to be documented further.

For more information, contact the owner of this repository.
This project is open-source and follows the GNU GPLv3 license; a copy of it can be found under 'Data'. Essentially, any derivative work must also be open source.
