import plan_executer
import jmeter_encoder

import time

import unittest
import data_processor.data_downloader
import config.config_reader as cr

class Test_test1(unittest.TestCase):
    test_plan_name = ""
    output_sample_name = "pe_testout.csv"

    start_script_path = ''
    start_script_name = 'setup.sh'
    start_file_name = 'TEST_PY_START2'
    server = ''
    username = ''
    password = ''
    generator_full_path = ''
    generator_parameter = ''
    plan_path = ''
    
    def test_parse_workload_to_vec(self):
        temp_encoder = jmeter_encoder.jmeter_encoder()
        temp_file = "pld.csv"
        group_name_vec = ['dslogin_in','dsbrowse_in','dspurchase_in','dsnewcustomer_in']
        workload_lengh = len(group_name_vec)
        temp_ret = temp_encoder.parse_workload_to_vec(temp_file, group_name_vec)
        print(temp_ret)

    @unittest.skip("skipping")
    def test_getname(self):
        temp_executer = plan_executer.plan_executer(self.start_script_path, self.start_script_name, self.server, self.username, self.password)

        temp_executer.start_perfmon_service(self.start_file_name)
        time.sleep(10)
        temp_executer.start_load_generator(self.plan_path, self.start_file_name)
        time.sleep(10)
        temp_executer.shutdown_test()

    def test_start_perfmon_only(self):
        temp_executer = plan_executer.plan_executer(self.start_script_path, self.start_script_name, self.server, self.username, self.password)
        temp_executer.start_perfmon_only("test_start2")
        time.sleep(5)
        temp_executer.stop_perfmon("test_start2")

    def test_clean_server_log(self):
        temp_executer = plan_executer.plan_executer(self.start_script_path, self.start_script_name, self.server, self.username, self.password)
        temp_executer.clear_server_log()

    def test_shutdown_test(self):
        temp_cfg = cr.config_reader()

        temp_executer = plan_executer.plan_executer(temp_cfg.start_script_path, 
                                                    temp_cfg.start_script_name, 
                                                    temp_cfg.server, 
                                                    temp_cfg.username, 
                                                    temp_cfg.password,
                                                    "")
        temp_executer.shutdown_test()
        

if __name__ == '__main__':
    unittest.main()