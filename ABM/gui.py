"""GUI Wrapper for Model"""

import tkinter as tk
from tkinter import ttk
from excel_export_summary_monkeys import save_summary
from excel_export_summary_humans import save_summary_humans, save_summary_human_demographics
from excel_export_summary_households import save_summary_households
from excel_export_density_plot import save_density_plot
from model import *
from families import demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list, moved_list
from humans import hh_size_list, human_birth_list, human_death_list, human_marriage_list,\
    single_male_list, married_male_list, \
    num_labor_list, total_migration_list, human_demographic_structure_list
from land import non_gtgp_part_list, gtgp_part_list, non_gtgp_area_list, gtgp_area_list, household_income_list
import os
from model import file_list, setting_list
from land import scenario_list, pes_span
from multiprocessing import Process, active_children
import time

run_token = []
running_list = []


def set_hh_file(h):
    """Sets size of human settlement"""
    if h == '400':
        household_file = 'hh_ascii400.txt'
    elif h == '800':
        household_file = 'hh_ascii800.txt'
    elif h == '100':
        household_file = 'hh_ascii100.txt'
    return household_file

def set_farm_file(fm):
    """Sets size of farmland"""
    if fm == '300':
        farm_file = 'farm_ascii300.txt'
    elif fm == '600':
        farm_file = 'farm_ascii600.txt'
    elif fm == '0':
        farm_file = 'ascii0.txt'
    return farm_file

def set_forest_file(fr):
    """Sets size of managed forest"""
    if fr == '200':
        forest_file = 'forest_ascii200.txt'
    elif fr == '400':
        forest_file = 'forest_ascii400.txt'
    elif fr == '0':
        forest_file = 'ascii0.txt'
    return forest_file

def set_filelist(h, fm, fr):
    file_list.append(set_hh_file(h))
    file_list.append(set_farm_file(fm))
    file_list.append(set_forest_file(fr))

def set_other_settings(fam):
    # index 0 = family, 1 = grid, 2 = run
    setting_list.append(fam)
    setting_list.append('With Humans')
    setting_list.append('Normal Run')  # First Run is an outdated setting

def set_scenario(sc, flat, dry, rice, before, after, brk):
    scenario_list.append(sc)
    if sc == 'Flat':
        scenario_list.append(flat)
    elif sc == 'Land Type':
        scenario_list.append(dry)
        scenario_list.append(rice)
    elif sc == 'Time':
        scenario_list.append(before)
        scenario_list.append(after)
        scenario_list.append(brk)

def set_pes_program_length(length):
    pes_span.append(length)

def execute():
    processes = []

    h = hh_input.get()
    fm = farm_input.get()
    fr = forest_input.get()
    fam = family_input.get()
    sc = scenario_input.get()
    flat = flat_input.get()
    dry = dry_input.get()
    rice = rice_input.get()
    before = before_input.get()
    after = after_input.get()
    brk = break_input.get()
    length = time_input.get()
    year = year_input.get()
    for i in list(range(int(thread_input.get()) - 1)):
        processes.append(Process(target=run_model, args=(h, fm, fr, fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year)))
    for p in processes:
        p.start()
        run_token.append(1)
        time.sleep(10)
    retry_run()

def execute_extended():
    processes = []

    h_list = ['400', '800', '0']
    fm_list = ['0', '300', '600']
    fr_list = ['0', '200', '400']
    fam = 20
    sc = 'Flat'
    flat = '270'
    dry = '200'
    rice = '400'
    before = '200'
    after = '400'
    brk = 4
    length = 8
    year = 1
    active_processes = 2
    p1 = Process(target=run_model, args=(h_list[0], fm_list[0], fr_list[0], fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year))
    p2 = Process(target=run_model, args=(h_list[0], fm_list[0], fr_list[1], fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year))
    p3 = Process(target=run_model, args=(h_list[0], fm_list[0], fr_list[2], fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year))
    p4 = Process(target=run_model, args=(h_list[0], fm_list[1], fr_list[0], fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year))
    p5 = Process(target=run_model, args=(h_list[0], fm_list[1], fr_list[1], fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year))
    p6 = Process(target=run_model, args=(h_list[0], fm_list[1], fr_list[2], fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year))
    p7 = Process(target=run_model, args=(h_list[0], fm_list[2], fr_list[0], fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year))
    p8 = Process(target=run_model, args=(h_list[0], fm_list[2], fr_list[1], fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year))
    p9 = Process(target=run_model, args=(h_list[0], fm_list[2], fr_list[2], fam, sc, flat, dry, rice, before, after,
                                                  brk, length, year))


        p1.start()
        time.sleep(10)
        p2.start()
        time.sleep(10)
        p1.join()
        p3.start()
        time.sleep(10)
        p2.join()
        p3.join()

def retry_run():
    while len(run_token) < int(run_count_input.get()):
        if len(active_children()) < int(thread_input.get()):
            h = hh_input.get()
            fm = farm_input.get()
            fr = forest_input.get()
            fam = family_input.get()
            sc = scenario_input.get()
            flat = flat_input.get()
            dry = dry_input.get()
            rice = rice_input.get()
            before = before_input.get()
            after = after_input.get()
            brk = break_input.get()
            length = time_input.get()
            year = year_input.get()
            p = Process(target=run_model, args=(h, fm, fr, fam, sc, flat, dry, rice, before, after,
                                                                 brk, length, year))
            p.start()
            run_token.append(1)
            time.sleep(10)


def run_model(h, fm, fr, fam, sc, flat, dry, rice, before, after, brk, length, year):
    """Identical to graph.py. Graph.py also directly runs the model."""
    set_filelist(h, fm, fr)
    set_other_settings(fam)
    set_scenario(sc, flat, dry, rice, before, after, brk)
    set_pes_program_length(length)

    monkey_population_list = []
    monkey_birth_count = []
    monkey_death_count = []

    model = Movement()  # run the model
    model_time = 73 * int(year) # 73 time-steps of 5 days each for 10 years, 730 steps total
    run = 1  # do not change this; it will automatically search for the first number-as-string not taken
    while os.path.isfile(os.getcwd() + '\\' + 'abm_export_summary_humans' + '_' + h + '_' + fm +
                         '_' + fr + '_' + str(run) + '.csv'):
        # if folder exists in current directory, loop up until it finds a unique number
        run += 1
    for t in range(model_time):  # for each time-step in the time we just defined,
        monkey_population_list.append(model.number_of_monkeys)
        monkey_birth_count.append(model.monkey_birth_count)
        monkey_death_count.append(model.monkey_death_count)
        model.step()  # see model.step() in model.py; monkey agents age, family-pixel agents move
        print('Loading Run', str(run), 'Progress', t, '/', model_time)
        if (t % 6 == 0 and t != 0) or t == 1:  # save beginning structure, then every 100 days thereafter
            save_summary(str(run), t, model.number_of_monkeys, model.monkey_birth_count, model.monkey_death_count,
                     demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list,
                         h, fm, fr)
            save_summary_humans(str(run), t, model.number_of_humans, len(human_birth_list), len(human_death_list),
                                sum(human_marriage_list), sum(num_labor_list),
                                len(single_male_list), len(married_male_list), sum(total_migration_list),
                                h, fm, fr
                                )  # 94 households
            save_summary_human_demographics(str(run), t, human_demographic_structure_list[0],
                                            human_demographic_structure_list[1],
                                            human_demographic_structure_list[2], human_demographic_structure_list[3],
                                            human_demographic_structure_list[4], human_demographic_structure_list[5],
                                            human_demographic_structure_list[6], human_demographic_structure_list[7],
                                            human_demographic_structure_list[8], human_demographic_structure_list[9],
                                            human_demographic_structure_list[10], human_demographic_structure_list[11],
                                            human_demographic_structure_list[12], human_demographic_structure_list[13],
                                            human_demographic_structure_list[14], human_demographic_structure_list[15],
                                            human_demographic_structure_list[16], human_demographic_structure_list[17],
                                            human_demographic_structure_list[18], human_demographic_structure_list[19],
                                            h, fm, fr)
            save_summary_households(str(run), t, sum(non_gtgp_part_list), sum(gtgp_part_list),
                                    sum(non_gtgp_part_list) / 94, sum(gtgp_part_list) / 94,
                                    sum(non_gtgp_area_list) / 94,
                                    sum(gtgp_area_list) / 94,
                                    sc, h, fm, fr
                                    )

    save_density_plot(moved_list, str(run), h, fm, fr)
    print('Run ' + str(run) + ' Done!')


        #if random_walk_graph_setting == True:  # disabled or enabled according to fnnr_config_file.py
#    # this should only be run with 1 family at a time or else the graphs will be messed up
#    for i in [1, 3, 5]:
#        if t == 73 * i:
#            save_density_plot(moved_list, str(i) + '_walk')
if __name__ == '__main__':
    root = tk.Tk()
    root.title('FNNR ABM')
    # canvas1 = tk.Canvas(root, width=300, height=300)
    status_text = tk.StringVar()
    status_text.set('FNNR ABM Model: PES Version')
    label = tk.Label(root, textvariable=status_text)  # main message
    label.grid(row=1, column=0, padx=10, pady=10)

    family_input = tk.Entry(root)
    family_input.grid(row=2, column=1)
    family_input.insert(0, 20)
    label1 = tk.Label(root, text="# of Monkey Families:")
    label1.grid(row=2, column=0, padx=10)

    year_input = tk.Entry(root)
    year_input.grid(row=3, column=1)
    year_input.insert(0, 20)
    label2 = tk.Label(root, text="# of Years to Run Model:")
    label2.grid(row=3, column=0, padx=10)

    #human_order = ['With Humans', 'Without Humans']
    #grid_setting = tk.StringVar()
    #grid_setting_menu = ttk.OptionMenu(root, grid_setting, human_order[0], *human_order)
    #grid_setting_menu.grid(row=4, column=1)
    #grid_setting_label = tk.Label(root, text="Run Setting:")
    #grid_setting_label.grid(row=4, column=0, padx=10)

    hh_order = ['100', '400', '800']
    hh_input = tk.StringVar()
    hh_setting_menu = ttk.OptionMenu(root, hh_input, hh_order[1], *hh_order)
    hh_setting_menu.grid(row=5, column=1)
    hh_setting_label = tk.Label(root, text="Human Settlement Area Buffer (m):")
    hh_setting_label.grid(row=5, column=0, padx=10)

    farm_order = ['0', '300', '600']
    farm_input = tk.StringVar()
    farm_menu = ttk.OptionMenu(root, farm_input, farm_order[1], *farm_order)
    farm_menu.grid(row=6, column=1)
    farm_label = tk.Label(root, text="Farmland Area Buffer (m):")
    farm_label.grid(row=6, column=0, padx=10)

    forest_order = ['0', '200', '400']
    forest_input = tk.StringVar()
    forest_menu = ttk.OptionMenu(root, forest_input, forest_order[1], *forest_order)
    forest_menu.grid(row=7, column=1)
    forest_label = tk.Label(root, text="Forest Area Buffer (m):")
    forest_label.grid(row=7, column=0, padx=10)

    scenario_order = ['Flat', 'Land Type', 'Time']
    scenario_input = tk.StringVar()
    scenario_menu = ttk.OptionMenu(root, scenario_input, scenario_order[0], *scenario_order)
    scenario_menu.grid(row=8, column=1)
    scenario_label = tk.Label(root, text="GTGP Scenario:")
    scenario_label.grid(row=8, column=0, padx=10)

    flat_order = [0, 270, 540]
    flat_input = tk.StringVar()
    flat_menu = ttk.OptionMenu(root, flat_input, flat_order[1], *flat_order)
    flat_menu.grid(row=9, column=1)
    flat_label = tk.Label(root, text="GTGP Flat Compensation (Yuan, Flat Scenario Only)")
    flat_label.grid(row=9, column=0, padx=10)

    dry_order = [100, 200, 300]
    dry_input = tk.StringVar()
    dry_menu = ttk.OptionMenu(root, dry_input, dry_order[1], *dry_order)
    dry_menu.grid(row=11, column=1)
    dry_label = tk.Label(root, text="GTGP Dry Land Compensation (Yuan, Land Type Scenario Only)")
    dry_label.grid(row=11, column=0, padx=10)

    rice_order = [300, 400, 500]
    rice_input = tk.StringVar()
    rice_menu = ttk.OptionMenu(root, rice_input, rice_order[1], *rice_order)
    rice_menu.grid(row=13, column=1)
    rice_label = tk.Label(root, text="GTGP Rice Paddy Compensation (Yuan, Land Type Scenario Only)")
    rice_label.grid(row=13, column=0, padx=10)

    before_order = [100, 200, 300, 400, 500]
    before_input = tk.StringVar()
    before_menu = ttk.OptionMenu(root, before_input, before_order[3], *before_order)
    before_menu.grid(row=14, column=1)
    before_label = tk.Label(root, text="Starting Compensation (Yuan, Time Scenario Only)")
    before_label.grid(row=14, column=0, padx=10)

    after_order = [100, 200, 300, 400, 500]
    after_input = tk.StringVar()
    after_menu = ttk.OptionMenu(root, after_input, after_order[1], *after_order)
    after_menu.grid(row=15, column=1)
    after_label = tk.Label(root, text="Ending Compensation (Yuan, Time Scenario Only)")
    after_label.grid(row=15, column=0, padx=10)

    break_order = [1, 2, 3, 4, 5, 10]
    break_input = tk.StringVar()
    break_menu = ttk.OptionMenu(root, break_input, break_order[3], *break_order)
    break_menu.grid(row=16, column=1)
    break_label = tk.Label(root, text="Breakpoint (Years, Time Scenario Only)")
    break_label.grid(row=16, column=0, padx=10)

    time_order = [1, 2, 4, 6, 8, 10, 20]
    time_input = tk.StringVar()
    time_menu = ttk.OptionMenu(root, time_input, time_order[4], *time_order)
    time_menu.grid(row=17, column=1)
    time_label = tk.Label(root, text="# of Years PES Program Lasts (All Scenarios)")
    time_label.grid(row=17, column=0, padx=10)
    time_label2 = tk.Label(root, text="(Note: Must be equal to or higher than Breakpoint if Time Scenario)")
    time_label2.grid(row=18, column=0, padx=10)

    divider_label = tk.Label(root, text="__________________________")
    divider_label.grid(row=19, column=0, padx=10)

    thread_order = [1, 2, 3, 4]
    thread_input = tk.StringVar()
    thread_menu = ttk.OptionMenu(root, thread_input, thread_order[1], *thread_order)
    thread_menu.grid(row=20, column=1)
    thread_label = tk.Label(root, text="# of Model Instances to Run Concurrently")
    thread_label.grid(row=20, column=0, padx=10)
    thread_label2 = tk.Label(root, text="(Note: Too High = Slower Results)")
    thread_label2.grid(row=21, column=0, padx=10)

    run_count_input = tk.Entry(root)
    run_count_input.grid(row=22, column=1)
    run_count_input.insert(0, 10)
    run_count = tk.Label(root, text="Total # of Runs:")
    run_count.grid(row=22, column=0, padx=10)

    run_button = tk.Button(root, text='Run Model', command=execute)
    run_button.grid(row=23,column=1, pady=10)

    divider_label = tk.Label(root, text="__________________________")
    divider_label.grid(row=24, column=1, padx=10)

    run_button = tk.Button(root, text='Run Model Up to 270 Times (Preset, ignore settings above)', command=execute_extended)
    run_button.grid(row=25,column=1, pady=10, padx=10)

    root.update_idletasks()
    root.mainloop()