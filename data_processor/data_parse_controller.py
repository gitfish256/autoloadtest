import subprocess
import shutil
import glob
import pandas
 
class data_parse_controller:


    def __init__(self, 
                 cur_datafolder_path,
                 parser_script_folder = None,
                 hold_load_file_path = None,
                 cut_before = None,
                 cut_after = None,
                 cfg = None):

        if cfg is None:
            self.cur_datafolder_path = cur_datafolder_path
            self.parser_script_folder = parser_script_folder
            self.hold_load_file_path = hold_load_file_path
            self.script_start_file_name = 'run_background.bat'
            self.cut_before = cut_before
            self.cut_after = cut_after
        else:
            self.cur_datafolder_path = cur_datafolder_path
            self.parser_script_folder = cfg.parser_script_folder
            self.hold_load_file_path = cfg.hold_load_file_path
            self.script_start_file_name = 'run_background.bat'
            self.cut_before = cfg.cut_before
            self.cut_after = cfg.cut_after


    def copy_script_to_datafolder(self):
       for file in glob.glob(self.parser_script_folder + '*'):
#            print file
            shutil.copy2(file, self.cur_datafolder_path)

    def copy_load_timeslot_to_datafolder(self):
        shutil.copy2(self.hold_load_file_path, self.cur_datafolder_path)

    def run_parser(self, initial_delay):
        script_full_path = self.cur_datafolder_path + self.script_start_file_name
        subprocess.call([script_full_path, str(initial_delay)], cwd = self.cur_datafolder_path)
       
    def get_output_file_path(self, interval, tail_name):
        file = glob.glob(self.cur_datafolder_path + '*' + str(interval) + '_' + tail_name + '.csv')
        if len(file) > 1:
            return("dup file")
        elif len(file) == 0: # some funny mix contains nothing
            return None
        else:
            return (file[0])

    def parse_data(self, initial_delay):
        self.copy_script_to_datafolder()
        self.run_parser(initial_delay)




