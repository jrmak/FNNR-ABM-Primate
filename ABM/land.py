from mesa.agent import Agent
import random
from fnnr_config_file import scenario, unit_comp_flat,\
    unit_comp_dry, unit_comp_rice, unit_comp_before, unit_comp_after, time_breakpoint, PES_span,\
    land_step_measure, no_pay_part, min_threshold, year_setting
from math import exp

household_income_list = [0] * 170
land_income_list = [0] * 170
non_gtgp_part_list = [0] * 170
gtgp_part_list = [0] * 170
non_gtgp_area_list = [0] * 170
gtgp_area_list = [0] * 170

class Land(Agent):
    """Sets land parcel agents"""

    def __init__(self, unique_id, model, hh_id, gtgp_enrolled,
                 age_1, gender_1, education_1, gtgp_dry, gtgp_rice, total_dry, total_rice,
                 land_type, land_time, plant_type, non_gtgp_output, pre_gtgp_output, hh_size,
                 non_gtgp_area, gtgp_area):

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
        self.hh_size = hh_size
        # print(self.hh_row, self.landpos, self.gtgp_enrolled, self.age_1, self.gender_1, self.education_1)

        self.gtgp_dry = gtgp_dry  # calculated in model.py
        self.gtgp_rice = gtgp_rice
        self.total_dry = total_dry
        self.total_rice = total_rice
        # print(self.gtgp_dry, self.gtgp_rice, self.total_dry, self.total_rice)

        self.non_gtgp_output = non_gtgp_output
        self.pre_gtgp_output = pre_gtgp_output
        self.non_gtgp_area = non_gtgp_area
        self.gtgp_area = gtgp_area

    def step(self):
        """Step behavior for LandParcelAgent"""
        if self.model.time == 1/73:
            if self.gtgp_enrolled == 0:
                non_gtgp_part_list[self.hh_id] += 1
                non_gtgp_area_list[self.hh_id] += (self.total_rice + self.total_dry - self.gtgp_rice - self.gtgp_dry)
                if non_gtgp_area_list[self.hh_id] == 0:
                    non_gtgp_area_list[self.hh_id] = 0.3  # minimum non-GTGP
            elif self.gtgp_enrolled == 1:
                gtgp_part_list[self.hh_id] += 1
                gtgp_area_list[self.hh_id] += self.gtgp_rice + self.gtgp_dry
            old_land_income = self.land_income  # resets yearly
            self.land_output()
            # self.gtgp_participation()
            from humans import hh_size_list
            self.hh_size = hh_size_list[self.hh_id]
            household_income_list[self.hh_id] = (household_income_list[self.hh_id]
                                                 + self.land_income)
            land_income_list[self.hh_id] = (land_income_list[self.hh_id]
                                                 + self.land_income)
        if random.random() < 1/(73):
        # if random.random() < 1/73:
            old_land_income = self.land_income  # resets
            old_gtgp_income = self.gtgp_net_income
            self.land_output()  # modifies self.land_income
            self.gtgp_participation()
            if self.gtgp_enrolled == 0:
                household_income_list[self.hh_id] = (household_income_list[self.hh_id]
                                                     + self.land_income - old_land_income)
                land_income_list[self.hh_id] = (land_income_list[self.hh_id]
                                                     + self.land_income - old_land_income)
            elif self.gtgp_enrolled == 1:
                household_income_list[self.hh_id] = (household_income_list[self.hh_id]
                                                     + self.gtgp_net_income - old_gtgp_income)
                land_income_list[self.hh_id] = (land_income_list[self.hh_id]
                                                + self.gtgp_net_income - old_gtgp_income)
            """
            if self.hh_id == 1:
                print('1', household_income_list[self.hh_id], self.plant_type, self.pre_gtgp_output, self.non_gtgp_output)
            if self.hh_id == 9:
                print('9', household_income_list[self.hh_id], self.plant_type, self.pre_gtgp_output, self.non_gtgp_output)
            """

    def land_output(self):
        """Calculates land output and income"""
        # unit prices are set in pseudo-code
        if int(self.plant_type) == 1:  # corn
            unit_price = 0.7
        elif int(self.plant_type) == 2:  # potato
            unit_price = 0.8
        elif int(self.plant_type) == 3:  # sweet potato
            unit_price = 0.9
        elif int(self.plant_type) == 4:  # rice
            unit_price = 2.3
        elif int(self.plant_type) == 5:  # abandoned fields
            unit_price = 0
        else:  # nuts, tea leaves, other vegetables, etc.
            unit_price = 1
        land_output = float(self.non_gtgp_output)
        if float(self.non_gtgp_output) == 0:
            land_output = self.pre_gtgp_output
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
        self.land_income = crop_income

    def convert_non_gtgp_to_gtgp(self):
        self.gtgp_enrolled = 1
        gtgp_part_list[self.hh_id] += 1
        if non_gtgp_part_list[self.hh_id] > 0:
            non_gtgp_part_list[self.hh_id] -= 1
        gtgp_area_list[self.hh_id] += self.gtgp_area
        non_gtgp_area_list[self.hh_id] -= self.non_gtgp_area

    def convert_gtgp_to_non_gtgp(self):
        self.gtgp_enrolled = 0  # changes gtgp enrollment
        non_gtgp_part_list[self.hh_id] += 1
        if gtgp_part_list[self.hh_id] > 0:
            gtgp_part_list[self.hh_id] -= 1
        gtgp_area_list[self.hh_id] -= self.gtgp_area
        non_gtgp_area_list[self.hh_id] += self.non_gtgp_area

    def gtgp_participation(self):
        minimum_non_gtgp = 0.3  # set in pseudo-code
        if self.total_dry in [-3, -4, '-3', '-4', None]:
            self.total_dry = 0
        if self.total_rice in [-3, -4, '-3', '-4', None]:
            self.total_rice = 0
        if self.gtgp_dry in [-3, -4, '-3', '-4', None]:
            self.gtgp_dry = 0
        if self.gtgp_rice in [-3, -4, '-3', '-4', None]:
            self.gtgp_rice = 0

        prob = exp(2.52 - 0.012 * float(self.age_1) - 0.29 * float(self.gender_1) + 0.01 * float(self.education_1)
                    + 0.001 * float(self.hh_size) - 2.45 * self.land_type + 0.0006 * float(self.gtgp_net_income)
                    + 0.04 * self.land_time)  # Shuang's GTGP conversion formula
        gtgp_part_prob = (prob / (prob + 1))
        if self.model.time > PES_span and self.gtgp_enrolled == 1:  # if PES payments have ended,
            gtgp_part_prob = no_pay_part * gtgp_part_prob # raise chances of reverting
            if random.random() < gtgp_part_prob * min_threshold:  # 0.3 is a minimum threshold
                self.convert_gtgp_to_non_gtgp()
        if self.model.time < PES_span:
            if non_gtgp_area_list[self.hh_id] < minimum_non_gtgp and self.gtgp_enrolled == 1:  # keep minimum non-GTGP area
                self.convert_gtgp_to_non_gtgp()
            if self.gtgp_enrolled == 0 and random.random() < gtgp_part_prob:  # GTGP conversion
                self.convert_non_gtgp_to_gtgp()
        # return self.gtgp_enrolled
