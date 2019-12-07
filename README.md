# FNNR-ABM-Primate

Welcome! This project seeks to understand population demographics and factors affecting the movement of Guizhou golden monkeys endemic to the Fanjingshan National Nature Reserve in Guizhou, China.
It uses Mesa, a library framework with tools designed to support agent-based modeling in Python 3.X.
EDIT: This model has been expanded since August and October to include human influences. Run the 8/15/18 version for the most bug-free version first, then run a more updated version of the model.

An overview of Mesa can be found at: https://mesa.readthedocs.io/en/master/overview.html
A more thorough doc can be found at: https://media.readthedocs.org/pdf/mesa/latest/mesa.pdf

Documentation for this project--as well as the source code available for download--can be found here. Please refer to the User's Manual or the QGIS Quickstart Guide.

Instructions for Running the Code:
1. Have Python 3.X installed and added to Windows PATH, as well as the Mesa library (which comes with dependencies such as numpy, pandas, and tornado).

!IMPORTANT!
*If you have errors running the code, make sure Mesa's edition is 0.8.3, and tornado's edition is 4.5.2.*

2. Download the code. Files are found in the ABM folder, though the Data folder has some files that are used for processing the data, using Microsoft Excel for some parts. Please refer to the later sections of the User's Manual, found in the parent directory of this repository, for more information.

3. Run 'gui.py'. Keep all settings at default if you're not sure what they are.

4. Once the model is run, 'run trim_grid35.py' on the 'abm_export_density_plot_with_humans_1.csv' file if you're only interested in the Yangaoping region (optional), then 'convert_csv_to_shapefile.py' on the trimmed version (rename the output shapefile within the code if you wish). Open the shapefile in ArcMap by using 'Add Data', select 'Zoom to Layer' from right-clicking the layer, and symbolize the layer with graduated colors. (While selecting the break type, you can also increase the sample size of the layer to 300,000 to avoid the warning.) The other results are freely available to analyze with Excel; some tools, such as 'kappa_batch.py', have been developed, but need to be documented further.

For more information, contact the owner of this repository.
This project is open-source and follows the GNU GPLv3 license; a copy of it can be found under 'Data'. Essentially, any derivative work must also be open source.
