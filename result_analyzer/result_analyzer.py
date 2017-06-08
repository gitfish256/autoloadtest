import utility.workload_info_connector as wl_con
import pandas
import subprocess

class result_analyzer(object):
    """description of class"""
#    Rscript_cwd = "k:\\BnOpti\\MARS_v1_ds2\\" 
#    Rscript_name = None
#    threshold = 500


    def __init__(self, Rscript_cwd, Rscript_name, threshold):
        self.Rscript_cwd = Rscript_cwd
        self.Rscript_name = Rscript_name
        self.threshold = threshold

    def get_predict_result(self, train_data, test_data, model, deps, total_population, threshold, parse_interval_in, run_name):
    #region get predict result part
#        full_workload_info_path = project_path + "\\" + self.input_workload_file_name
        Rscript_path = self.Rscript_cwd + self.Rscript_name 
        R_result = subprocess.Popen(["Rscript", 
                                Rscript_path, 
                                model, 
                                train_data,
                                test_data,
                                deps,
                                str(total_population),
                                str(threshold),
                                str(parse_interval_in),
                                run_name],
                                stdout=subprocess.PIPE,
                                cwd = self.Rscript_cwd)

        out, err = R_result.communicate()
        return out

    def get_next_workload(self, workload_file_path, total_population, deps, threshold):
    #region get predict result part
#        full_workload_info_path = project_path + "\\" + self.input_workload_file_name
        Rscript_path = self.Rscript_cwd + self.Rscript_name 

        R_result = subprocess.Popen(["Rscript", 
                                Rscript_path, 
                                workload_file_path, 
                                str(total_population),
                                deps,
                                str(threshold)],
                                stdout=subprocess.PIPE,
                                cwd = self.Rscript_cwd)

        out, err = R_result.communicate()
        return out

    def get_next_random_workload(self, workload_file_path, indeps_count):
        Rscript_path = self.Rscript_cwd + self.Rscript_name 

        R_result = subprocess.Popen(["Rscript", 
                                Rscript_path, 
                                workload_file_path, 
                                str(indeps_count)],
                                stdout=subprocess.PIPE,
                                cwd = self.Rscript_cwd)

        out, err = R_result.communicate()
        return out

