# FNNR-ABM-Primate

Welcome! This project seeks to understand population demographics and factors affecting the movement of Guizhou golden monkeys endemic to the Fanjingshan National Nature Reserve in Guizhou, China.
It uses Mesa, a library framework with tools designed to support agent-based modeling in Python 3.X.

An overview of Mesa can be found at: https://mesa.readthedocs.io/en/master/overview.html
A more through doc can be found at: https://media.readthedocs.org/pdf/mesa/latest/mesa.pdf

Documentation for this project--as well as the source code available for download--can be found on this page.

Instructions for Running the Code:
1. Have Python 3.X installed, as well as the Mesa (which comes with dependencies such as numpy, pandas, and tornado) and matplotlib libraries.
If you have errors running the code and it is library-related, make sure Mesa's edition is 0.8.3, and tornado's edition is 4.5.2.

2. Download the code. Files are found in the ABM folder.

3a. Run 'server.py' to launch a web browser with an interactive visualization module of monkey movement.
Monkey movements are semi-randomized, and based on the weighted value of their 8-neighbor surroundings.
This weighted value is currently determined by elevation (changeable in code; requires a raster layer converted to an ASCII file).

3b. Run 'graph.py' to see population demographic charts after 1 year, or 73 time-steps (changeable in code).

This project is incomplete.
For more information, contact the owner of this repository.
