import pandas
import sys

project_path = sys.path[0] + "\\.."
sys.path.append(project_path)

import config.config_reader as cr

class summary_controller(object):
    """description of class"""
    timestamp_name = "T_Time"
    #timestamp_name = "James_Time"

    def __init__(self, input_summary_file):
        self.sum_df = pandas.read_csv(input_summary_file)
        self.T_CPU_core = 'T_CPU'
        self.M_CPU_core = 'M_CPU'

    def get_data_by_deps(self, deps_in):
        return self.sum_df[deps_in]

    def get_timestamp(self):
        return self.sum_df[self.timestamp_name]