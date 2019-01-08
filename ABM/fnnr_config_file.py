"""
Configuration Settings
"""

"""
Running the model
"""
# numbers should be whole positive integers and strings (text) or floats (decimal numbers)
family_setting = 20  # number of monkey families; default/recommended is 20; set to 1 for random walk mapping
year_setting = 10  # number of years the model will run, as an integer multiple of 73 5-day time-steps; default is 10
human_setting = "with_humans"  # "with_humans" or "without_humans"; default is "with_humans"
run_setting = "normal_run"  # "normal_run" or "first_run"; default is "normal_run"
random_walk_graph_setting = False  # not a string; set this to True only if family_setting = 1; default is False
plot_setting = False  # pops up monkey demographic graphs that were exported to the Excel files; default is False

if random_walk_graph_setting == True and family_setting != 1:
    print("Please set the random_walk_graph_setting to False if you are running the model with multiple families.")

"""
Configuring randomwalk.py
"""
model_exported_density_plot_file = 'export_density_plot_with_humans_1.csv'
# change the 1 to the number of your model run
# make sure name is a string ending in .csv
# example: 'export_density_plot_with_humans_1.csv'
