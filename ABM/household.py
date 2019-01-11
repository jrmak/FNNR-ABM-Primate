# !/usr/bin/python
"""
This document imports household data from the Excel file containing Shuang's survey results and determines behavior
for household agents.
"""

from mesa.agent import Agent
import random
from fnnr_config_file import PES_span

minimum_non_gtgp = 0.3

class Household(Agent):
    # can enroll or abandon GTGP participation
    def __init__(self, unique_id, model, gtgp_part_prob, hh_id, head_of_household,
                 age_1, gender_1, education_1, total_rice, total_dry, gtgp_rice, gtgp_dry,
                 ):
        super().__init__(unique_id, model)
        self.gtgp_part_prob = gtgp_part_prob
        self.hh_id = hh_id  # unique_id is in order; hh_id refers to hh_citizens.csv
        self.head_of_household = head_of_household
        self.age_1 = age_1
        self.gender_1 = gender_1
        self.education_1 = education_1
        self.total_rice = total_rice
        self.total_dry = total_dry
        self.gtgp_rice = gtgp_rice
        self.gtgp_dry = gtgp_dry

    def step(self):
        # human aging/demographic behavior
        if self.head_of_household in head_of_household_list:
            self.gtgp_check()
        else:
            pass


    def gtgp_check(self):
        non_gtgp_area = (float(self.total_rice) + float(self.total_dry)) \
                        - (float(self.gtgp_dry) + float(self.gtgp_rice))


        if non_gtgp_area < minimum_non_gtgp:
            self.gtgp_part_prob = 0
        if self.model.time > PES_span:
            self.gtgp_part_prob = no_pay_part * self.gtgp_part_prob

        self.gtgp_net_income = comp_amount - crop_income
        self.land_income = comp_amount + crop_income


        prob = exp(2.52 - 0.012 * float(self.age_1) - 0.29 * float(self.gender_1) + 0.01 * float(self.education_1)
                   + 0.001 * float(self.hh_size) - 2.45 * self.land_type * 0.0006 * float(self.gtgp_net_income)
                   + 0.04 * self.land_time)
        self.gtgp_part_prob = prob / prob + 1

        if random() < gtgp_part_prob:
            self.gtgp_enrolled = 1
            if self.hh_id not in gtgp_part_list:
                gtgp_part_list.append(self.hh_id)
        return self.gtgp_enrolled  # 0 or 1

