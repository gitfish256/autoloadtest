import unittest
import data_downloader
import data_parse_controller
import summary_controller
import shutil
import glob
import subprocess

import config.config_reader as cfg

class Test_test1(unittest.TestCase):
    server = ''
    username = ''
    password = ''
    test_folder_info_path = ''
    test_folder_info_name = 'temp_test_name.txt'

    test_dest_folder = ''
    cur_datafolder_name = ''
    parser_script_folder = ''
    hold_load_file_path = ''

    def test_getname(self):
        temp_down = data_processor.data_downloader.data_downloader(self.server, self.username, self.password, self.test_folder_info_path, self.test_folder_info_name)
        print(temp_down.get_current_test_name())

    def test_get_counter_data(self):
        temp_down = data_processor.data_downloader.data_downloader(self.server, self.username, self.password, self.test_folder_info_path, self.test_folder_info_name)

    def test_get_apache_data(self):
        temp_down = data_processor.data_downloader.data_downloader(self.server, self.username, self.password, self.test_folder_info_path, self.test_folder_info_name)
        temp_dest_folder = temp_down.get_current_test_name()

        temp_down.download_apache_log(self.test_dest_folder, temp_dest_folder)


    def test_run_parser(self):
        temp_parser = data_processor.data_parse_controller.data_parse_controller(
            self.cur_datafolder_name,
            self.parser_script_folder,
            self.hold_load_file_path)
        temp_parser.copy_load_timeslot_to_datafolder()
        temp_parser.copy_script_to_datafolder()
        temp_parser.run_parser(60, 'test_tail')
    
    def test_get_result_file(self):
        temp_parser = data_processor.data_parse_controller.data_parse_controller(
            self.cur_datafolder_name,
            self.parser_script_folder,
            self.hold_load_file_path)
        temp_out = temp_parser.get_output_file_path(60, 'test_tail')
 #       self.assertEqual(temp_out, 1, msg = '{}'.format(temp_out))

    def test_get_result(self):
        temp_parser = data_processor.data_parse_controller.data_parse_controller(
            self.cur_datafolder_name,
            self.parser_script_folder,
            self.hold_load_file_path)
        temp_parser.copy_load_timeslot_to_datafolder()
        temp_parser.copy_script_to_datafolder()
#        temp_parser.run_parser(60, 'test_tail')
        input_workload_file_name = "test_load.csv"

        temp_summary_file = temp_parser.get_output_file_path(60, 'test_tail')


        #region get predict result part
        Rscript_path = ""
        project_path = ""
        full_workload_info_path = project_path + "\\" + input_workload_file_name
        R_result = subprocess.Popen(["Rscript", 
                                Rscript_path, 
                                "MLR", 
                                temp_summary_file,
                                temp_summary_file,
                                "dspurchase_rpt",
                                str(100),
                                full_workload_info_path],
                                stdout=subprocess.PIPE,
                                cwd = "")

        out, err = R_result.communicate()
        print(out)
        print(err)
    

    def test_collect_result(self):
        temp_cfg = cfg.config_reader()
        temp_down = data_downloader.data_downloader(cfg = temp_cfg)

        temp_down.collect_result("")


if __name__ == '__main__':
    unittest.main()
