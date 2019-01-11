from fnnr_config_file import scenario_unit_comp

household_income_list = 0 * [170]
land_income_list = 0 * [170]


class LandParcelAgent(Agent):
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
        old_land_income = self.land_income  # resets yearly
        self.output()  # modifies self.land_income
        self.gtgp_participation()
        self.non_gtgp_count(nongtgplist, gtgplist)
        self.gtgp_count(nongtgplist, gtgplist)
        household_income_list[self.hh_id] = (household_income_list[self.hh_id]
                                             + self.land_income - old_land_income)
            land_income_list[self.hh_id] = (land_income_list[self.hh_row - 1]
                                                 + self.land_income - old_land_income)


    def land_output(self):
        """Calculates land output and income"""
        if self.plant_type == 1:
            unit_price = 0.7  # set in pseudo-code
        elif self.plant_type == 2:
            unit_price = 0.8
        elif self.plant_type == 3:
            unit_price = 0.9
        elif self.plant_type == 4:
            unit_price = 2.3
        elif self.plant_type == 5:
            unit_price = 0
        else:
            unit_price = 1
        if self.gtgp_enrolled == 1:
            try:
                land_output = float(self.pre_gtgp_output)
            except ValueError:
                pass
        else:
            land_output = float(self.non_gtgp_output)
        crop_income = land_output * unit_price

        unit_comp = scenario_unit_comp  # see fnnr_config_file

        self.land_area = float(self.total_dry) + float(self.total_rice)
        comp_amount = self.land_area * unit_comp

        self.gtgp_net_income = comp_amount - crop_income
        self.land_income = comp_amount + crop_income

    def gtgp_participation(self):
        minimum_non_gtgp = 0.3  # set in pseudo-code
        if self.total_dry is None:  # not applicable to 2014 data
            self.total_dry = 0
        if self.total_rice is None:
            self.total_rice = 0
        if self.gtgp_dry is None:
            self.gtgp_dry = 0
        if self.gtgp_rice is None:
            self.gtgp_rice = 0
        non_gtgp_area = (float(self.total_dry) + float(self.total_rice)) \
        - (float(self.gtgp_dry) + float(self.gtgp_rice))
        self.hh_size = len(return_values(self.hh_row, 'age'))
        try:
            prob = exp(2.52 - 0.012 * float(self.age_1) - 0.29 * float(self.gender_1) + 0.01 * float(self.education_1)
                        + 0.001 * float(self.hh_size) - 2.45 * self.land_type * 0.0006 * float(self.gtgp_net_income)
                        + 0.04 * self.land_time)
        except:
            prob = 0
            pass
        gtgp_part_prob = prob / (prob + 1)
        if non_gtgp_area < minimum_non_gtgp:
            gtgp_part_prob = 0
            if self.hh_id in gtgp_part_list:
                gtgp_part_list.remove(self.hh_id)
        if random() < gtgp_part_prob:
            self.gtgp_enrolled = 1
            if self.hh_id not in gtgp_part_list:
                gtgp_part_list.append(self.hh_id)
        return self.gtgp_enrolled