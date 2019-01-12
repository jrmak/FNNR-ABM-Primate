from mesa.agent import Agent
import random
from fnnr_config_file import scenario, unit_comp_flat,\
    unit_comp_dry, unit_comp_rice, unit_comp_before, unit_comp_after, time_breakpoint

household_income_list = 170 * [0]
land_income_list = 170 * [0]
non_gtgp_part_list = []
gtgp_part_list = []
non_gtgp_area_list = 170 * [0]
gtgp_area_list = 170 * [0]

class Land(Agent):
    """Sets land parcel agents"""

    def __init__(self, unique_id, model, hh_id, gtgp_enrolled,
                 age_1, gender_1, education_1, gtgp_dry, gtgp_rice, total_dry, total_rice,
                 land_type, land_time, plant_type, non_gtgp_output, pre_gtgp_output):

        super().__init__(unique_id, model)
        self.hh_id = hh_id
        self.gtgp_enrolled = gtgp_enrolled  # inherited from HouseholdAgent
        self.age_1 = age_1  # calculated in model.py
        self.gender_1 = gender_1
        self.education_1 = education_1
        self.land_type = land_type
        self.land_time = land_time
        self.gtgp_net_income = 0  # calculated later
        self.land_income = 0  # calculated later
        self.plant_type = plant_type
        # print(self.hh_row, self.landpos, self.gtgp_enrolled, self.age_1, self.gender_1, self.education_1)

        self.gtgp_dry = gtgp_dry  # calculated in model.py
        self.gtgp_rice = gtgp_rice
        self.total_dry = total_dry
        self.total_rice = total_rice
        # print(self.gtgp_dry, self.gtgp_rice, self.total_dry, self.total_rice)

        self.non_gtgp_output = non_gtgp_output
        self.pre_gtgp_output = pre_gtgp_output

    def step(self):
        """Step behavior for LandParcelAgent"""
        if self.model.time in list(range(21)):
            print('a year has passed')
            old_land_income = self.land_income  # resets yearly
            self.output()  # modifies self.land_income
            self.gtgp_participation()
            household_income_list[self.hh_id] = (household_income_list[self.hh_id]
                                                 + self.land_income - old_land_income)
            land_income_list[self.hh_id] = (land_income_list[self.hh_id]
                                                 + self.land_income - old_land_income)

    def land_output(self):
        """Calculates land output and income"""
        # unit prices are set in pseudo-code
        if self.plant_type == 1:  # corn
            unit_price = 0.7
        elif self.plant_type == 2:  # potato
            unit_price = 0.8
        elif self.plant_type == 3:  # sweet potato
            unit_price = 0.9
        elif self.plant_type == 4:  # rice
            unit_price = 2.3
        elif self.plant_type == 5:  # abandoned fields
            unit_price = 0
        else:  # nuts, tea leaves, other vegetables, etc.
            unit_price = 1
        if self.gtgp_enrolled == 1:
            try:
                land_output = float(self.pre_gtgp_output)
            except ValueError:
                pass
        else:
            land_output = float(self.non_gtgp_output)
        crop_income = land_output * unit_price

        self.land_area = float(self.total_dry) + float(self.total_rice)

        if scenario.lower() == 'flat':
            comp_amount = self.land_area * unit_comp_flat
        elif scenario.lower() == 'land_type':  # see fnnr_config_file
            if int(self.land_type) == 1:
                comp_amount = self.land_area * unit_comp_dry
            elif int(self.land_type) == 2:
                comp_amount = self.land_area * unit_comp_rice
        elif scenario.lower() == 'time':
            if self.model.time < scenario_breakpoint:
                comp_amount = self.land_area * unit_comp_before
            elif self.model.time > time_breakpoint:
                comp_amount = self.land_area * unit_comp_after

        self.gtgp_net_income = comp_amount - crop_income
        self.land_income = comp_amount + crop_income

    def gtgp_participation(self):
        minimum_non_gtgp = 0.3  # set in pseudo-code
        if self.total_dry is None:
            self.total_dry = 0
        if self.total_rice is None:
            self.total_rice = 0
        if self.gtgp_dry is None:
            self.gtgp_dry = 0
        if self.gtgp_rice is None:
            self.gtgp_rice = 0
        non_gtgp_area = (float(self.total_dry) + float(self.total_rice)) \
        - (float(self.gtgp_dry) + float(self.gtgp_rice))  # non_gtgp_area is for the household
        gtgp_area = float(self.gtgp_dry) + float(self.gtgp_rice)
        prob = exp(2.52 - 0.012 * float(self.age_1) - 0.29 * float(self.gender_1) + 0.01 * float(self.education_1)
                    + 0.001 * float(self.hh_size) - 2.45 * self.land_type * 0.0006 * float(self.gtgp_net_income)
                    + 0.04 * self.land_time)
        gtgp_part_prob = prob / (prob + 1)
        if self.model.time > PES_span and self.gtgp_enrolled == 1:  # if PES payments have ended,
            self.gtgp_part_prob = no_pay_part * self.gtgp_part_prob # raise chances of reverting
            if random() < gtgp_part_prob * 0.3:  # 0.3 is a minimum threshold
                self.gtgp_enrolled = 0
                gtgp_area_list[self.hh_id] -= gtgp_area
                non_gtgp_area_list[self.hh_id] += non_gtgp_area
                if self.hh_id in gtgp_part_list:
                    gtgp_part_list.remove(self.hh_id)
                if self.hh_id not in non_gtgp_part_list:
                    non_gtgp_part_list.append(self.hh_id)
        if non_gtgp_area < minimum_non_gtgp:
            gtgp_part_prob = 0
            if self.hh_id in gtgp_part_list:
                gtgp_part_list.remove(self.hh_id)
                if self.hh_id not in non_gtgp_part_list:
                    non_gtgp_part_list.append(self.hh_id)
        if random() < gtgp_part_prob:
            self.gtgp_enrolled = 1
            gtgp_area_list[self.hh_id] += gtgp_area
            non_gtgp_area_list[self.hh_id] += non_gtgp_area
            if self.hh_id in non_gtgp_part_list:
                    non_gtgp_part_list.remove(self_hh_id)
            if self.hh_id not in gtgp_part_list:
                gtgp_part_list.append(self.hh_id)
        # return self.gtgp_enrolled