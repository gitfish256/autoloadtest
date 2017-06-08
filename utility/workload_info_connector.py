import pandas
import os
import config.config_reader as cr
class workload_info_connector(object):
    """description of class"""


 #   workload_data = None
#    file_path = ""

    def __init__(self, file_path):
        temp_cr = cr.config_reader()

        self.workload_mix = temp_cr.group_name_vec

        self.workload_header = ["model_info", 
                            "total_population", 
                            "status"] + self.workload_mix
        self.predict_header = ["pred_result"]

        self.result_header = ["fitness", 
                        "output_mean", 
                        "result"]
     
        self.workload_info_header = self.workload_header + self.predict_header + self.result_header
    

        if os.path.exists(file_path):
            self.file_path = file_path
            self.workload_data = pandas.read_csv(file_path)

        else:
             self.file_path = file_path
             self.workload_data = pandas.DataFrame(None, columns = self.workload_info_header)

    def get_total_row(self):
        return len(self.workload_data)

    def get_row_by_model_info(self, model_info_in):
        return 


    def append_line_to_data(self, line_to_write):
        self.workload_data.loc[len(self.workload_data)] = line_to_write
        return True

    def read_line_by_row(self, row_number):
        return self.workload_data.loc[row_number]

    def read_value(self, row_number, col_name):
        return self.workload_data.loc[row_number, col_name]


    def write_value(self, row_number, col_name, value):
        self.workload_data.loc[row_number, col_name] = value
        return True

    def save_to_file(self):
        self.workload_data.to_csv(self.file_path, index = False)

    def get_result_from_series(self, input_series):
        return (input_series.loc[self.result_header])

    def get_workload_from_series(self, input_series):
        return (input_series.loc[self.workload_header])

    def parse_predict_result_to_series(self, input_string):
        temp_list = input_string.split(';')
        temp_series = pandas.Series(data = temp_list, index = self.workload_info_header)
        return (temp_series)

    def get_cur_row_number_by_name(self, input_current_run_name):
        row_key = self.workload_data[self.workload_data['model_info'].str.contains(input_current_run_name)]['model_info']
        match_list = self.workload_data[self.workload_data['model_info'] == row_key.values[0]].index.tolist()
        if len(row_key.values.tolist()) > 1:
            print("dup row_key")
        if len(match_list) > 1:
            print("dup match_list")
        return match_list[0]


