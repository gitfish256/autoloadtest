import os
import re
import utility as util
import utility.remote_connector as rc
import utility.multi_connector as mc
import config.config_reader as cr
import plan_encoder.jmeter_encoder as jmeter_encoder

class pre_processor(object):
    """description of class"""

    def __init__(self, cfg, tl_list):
        self.cfg = cfg
        if (cfg.is_multi_mode):
            self.temp_connector_list = mc.multi_connector(cfg.node_ip_list, cfg.node_user_list, cfg.pass_list)
        else:
            self.temp_connector = rc.remote_connector(self.cfg.server, self.cfg.username, self.cfg.password)
        self.cur_run_info = None
        self.output_plan_name = None
        self.read_run_name = None
        self.total_duration = None
        self.temp_encoder = None
        self.tl_list = tl_list


    '''
    should include:
        read test plan list;
        deploy version;
        run pre process script;
        reboot;
    '''

    def encode_workload(self):
        # region workload encoding part
         
        self.cur_run_info = self.tl_list.get_next_test()
        if self.cur_run_info is None:
            return False
        self.output_plan_name = self.cur_run_info['test_plan_path']
        temp_encoder = jmeter_encoder.jmeter_encoder()
        self.read_run_name = self.cur_run_info['run_name']

        #hold_load_time_list.append([temp_initial_delay + startup_time, temp_initial_delay + startup_time + hold_time])
        hold_load_time_list = []
        hold_load_time_list.append([self.cur_run_info['initial_delay'] + self.cur_run_info['startup_time'], 
                                    self.cur_run_info['initial_delay'] + self.cur_run_info['startup_time'] + self.cur_run_info['hold_time'] + self.cur_run_info['shutdown_time']]) 

        self.total_duration = self.cur_run_info['startup_time'] + self.cur_run_info['hold_time'] + self.cur_run_info['shutdown_time']
#        temp_encoder.write_timeslots_to_file(hold_load_time_list, self.cfg.hold_load_file_path, True)
        self.temp_encoder = temp_encoder
        return True

    def deploy_system(self):
        if self.cfg.is_script_deployment is False:
            system_path = self.cur_run_info['version_file_path']
            deploy_path = self.cur_run_info['deploy_path']
            system_path.encode("ascii", "ignore")
            system_path = re.sub("(u2018|u2019)", "", system_path)
 
           
            #if (os.path.isdir(system_path)):
            cp_command = "cp -r " + system_path + " " + deploy_path
            #else:
            #    cp_command = "cp " + system_path + " " + deploy_path
            ret = self.temp_connector.send_command(cp_command, True)
            print(ret)
        else:
            deploy_script = self.cur_run_info['deploy_script']
            ret = self.temp_connector.send_command(deploy_script, True)
            print(ret)

        if self.cfg.is_manual_start is True:
            start_script = self.cur_run_info['start_script']
            ret = self.temp_connector.send_command(start_script, True, False)
            print(ret)


    def run_pre_script(self):
        pre_script_path = self.cur_run_info['pre_script']
        if (self.cfg.is_multi_mode):
            self.temp_connector
        print (self.temp_connector.send_command(pre_script_path, True))


    



