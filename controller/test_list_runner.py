import time
import sys
import os
import subprocess
import pandas
import re
import shutil
#from HQ_controller.config import config

project_path = sys.path[0] + "\\.."
sys.path.append(project_path)
import data_processor.data_downloader as data_downloader
import data_processor.data_parse_controller as data_parser
import plan_encoder.plan_executer as plan_executer
import plan_encoder.jmeter_encoder as jmeter_encoder
import utility.utility as util

import utility.test_list_connector as tl_con
import utility.remote_connector as rc
import result_analyzer.result_analyzer as result_analyzer
import config.config_reader as cr
import pre_processor.pre_processor as pre_pro
import post_processor.post_processor as post_pro

class test_list_runner(object):
    """description of class"""

    def __init__(self, 
                 test_list_file_name,
                 cfg_file_name):

        self.cfg = cr.config_reader(cfg_file_name)
        self.tl_list = tl_con.test_list_connector(test_list_file_name)
        self.pre_processor = pre_pro.pre_processor(self.cfg, self.tl_list)
        self.post_processor = post_pro.post_processor(self.cfg, None)
        self.downloader = data_downloader.data_downloader(cfg = self.cfg)
        self.jmeter_file_path = None
        self.temp_rc = rc.remote_connector(cfg = self.cfg)
        self.data_parser = data_parser.data_parse_controller(None, cfg = self.cfg)

    '''
    should include:
        read test plan list;
        deploy version;
        run pre process script;
        reboot;
    '''
    def run_pre_process(self):
        temp_pre = self.pre_processor
        has_workload = temp_pre.encode_workload()
        if has_workload is False:
            return False
        #temp_pre.deploy_system()
        #raw_input("Press Enter to get to run test...")
        temp_pre.run_pre_script()
        return True

#        time.sleep(10)

#        self.shutdown_test()
#        time.sleep(10)

    '''
    include:
        run setup script;
        run jmeter;
    '''
    def run_test(self):
        

        temp_exec = plan_executer.plan_executer(cfg_file = self.cfg)
        temp_exec.start_perfmon_service(self.pre_processor.cur_run_info['run_name'])
        time.sleep(10)
        jmeter_file_name = 'jmeter_' + self.pre_processor.cur_run_info['run_name'] + '.csv'
        self.jmeter_file_path = jmeter_file_name
        temp_exec.start_load_generator(self.pre_processor.cur_run_info['test_plan_path'],
                                       jmeter_file_name)

        time.sleep(5)


#        wait_for_plan_end_time = 10

#        print('sleep for {}'.format(wait_for_plan_end_time))
#        time.sleep(wait_for_plan_end_time)

    '''
    include:
        reboot;
    '''
    def wait_shutdown_test(self):
        temp_exec = plan_executer.plan_executer(cfg_file = self.cfg)
        time.sleep(10)
        temp_exec.shutdown_test()
        time.sleep(10)

    '''
    include:
        collect data;
        run post_process script (clean up);
        reboot;
    '''
    def run_post_process(self):
        ret = self.downloader.collect_result(self.jmeter_file_path)
        if ret is True:
            self.tl_list.test_list_info.loc[self.tl_list.cur_row_index, 'status'] = 'checked'
            self.tl_list.save_to_file()

        self.data_parser.cur_datafolder_path = self.downloader.cur_datafolder_path
        self.data_parser.parse_data(self.pre_processor.cur_run_info['initial_delay'])
        self.post_processor.cur_run_info = self.pre_processor.cur_run_info
        self.post_processor.run_post_script() 
        return ret


    '''
        use post process script to clean the system before run the test
    '''
    def clean_system(self):
        self.post_processor.run_post_script()

if __name__ == '__main__':
    test_runner = test_list_runner("DS2testlist.csv", "DS2_auto_config.cfg")
#    test_runner = test_list_runner("JMS_testlist_RQ6.csv", "JMS_auto_config.cfg")

    has_next = test_runner.run_pre_process()
#    raw_input("Press Enter to get to run test...")
    while has_next is True:
#        test_runner.wait_shutdown_test()
        test_runner.temp_rc.check_online(120000, is_reboot = False)
        
        test_runner.run_test()
        test_runner.wait_shutdown_test()
        test_runner.temp_rc.check_online(120000)
        test_runner.run_post_process()
        test_runner.wait_shutdown_test()
        test_runner.temp_rc.check_online(120000)
        has_next = test_runner.run_pre_process()

      

    print "all over"

