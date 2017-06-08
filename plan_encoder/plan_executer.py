import paramiko
import time
import config.config_reader as cr
from subprocess import call
from utility.remote_connector import remote_connector
import glob

class plan_executer:


    start_monitor_script_name = 'monitor_setup.sh'
    monitor_pid_info_file_name = 'temp_monitor_pid.log'
    cleanup_script = ""
    generator_full_path = ''
    generator_parameter = ''


    #if no cfg file then use the parameters, or use cfg file
    def __init__(self, start_script_path_in = None, 
                 start_script_name_in = None,
                 server_in = None, 
                 uname_in = None, 
                 pass_in = None, 
                 monitor_pid_info_file_name = None, 
                 cfg_file = None):

        if cfg_file is None:
            self.start_script_name = start_script_name_in
            self.start_script_path = start_script_path_in
            self.server = server_in
            self.username = uname_in
            self.password = pass_in
            self.monitor_pid_info_file_name = monitor_pid_info_file_name
        else:
            cfg = cfg_file
            self.start_script_name = cfg.start_script_name
            self.start_script_path = cfg.start_script_path
            self.server = cfg.server
            self.username = cfg.username
            self.password = cfg.password
            self.monitor_pid_info_file_name = cfg.monitor_pid_info_file_name
            self.start_monitor_script_name = ""
            self.monitor_pid_info_file_name = 'temp_monitor_pid.log'
            self.cleanup_script = cfg.clean_script_name
            self.generator_full_path = cfg.generator_full_path
            self.generator_parameter = ""

    def start_perfmon_service(self, start_file_name_in):
        if not start_file_name_in:
            print("mon folder null\n")
            return 0
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = self.server, username = self.username, password = self.password)
#        stdin, stdout, stderr = ssh.exec_command('echo %s | sudo -S ls -a' % self.password)
        #stdin, stdout, stderr = ssh.exec_command('cd ' + start_script_path)
        stdin, stdout, stderr = ssh.exec_command((('cd ' + self.start_script_path) + ';' + 'echo %s | sudo -S ' + self.start_script_path + self.start_script_name + ' ' + start_file_name_in) % self.password)
        print("out")
        for temp in stdout:
            print(temp.replace(u"\u2018", "'").replace(u"\u2019", "'"))
        print("err")
        for temp in stderr:
            print(temp.replace(u"\u2018", "'").replace(u"\u2019", "'"))
        ssh.close()
        return 1

    def start_perfmon_only(self, start_file_name_in):
        if not start_file_name_in:
            print("mon folder null\n")
            return 0
        ssh = remote_connector(self.server, self.username, self.password)
        ssh.send_command((('cd ' + self.start_script_path) + ';' + 'echo %s | sudo -S ' + self.start_script_path + self.start_monitor_script_name + ' ' + start_file_name_in) % self.password)
        
    def stop_perfmon(self, start_file_name_in):
        if not start_file_name_in:
            print("dest folder null\n")
            return 0
        ssh = remote_connector(self.server, self.username, self.password)
        pid_list = ssh.send_command('cat ' + self.start_script_path + '*' + start_file_name_in + '/'
                                    + self.monitor_pid_info_file_name)
        for i in pid_list:
            ssh.send_command(('echo %s | sudo -S kill ' + i) % self.password)

    def clear_server_log(self):
        server_log_path = "//var//log//tomcat7//"
          
        ssh = remote_connector(self.server, self.username, self.password)
        ssh.send_command(('cd ' + server_log_path + ';' + 
                         'echo %s | sudo -S cp //dev//null localhost_access_log*.txt') % self.password) 
        ssh.send_command(('cd ' + server_log_path + ';' + 
                         'echo %s | sudo -S cp //dev//null gc.log') % self.password) 



    def construct_full_generator_command(self, test_plan_name, result_file_name):
        full_command = self.generator_full_path + ' -n -t ' + test_plan_name + ' -l ' + result_file_name

        return full_command


    def start_load_generator(self, test_name, result_file_name):
        full_command = self.construct_full_generator_command(test_name, result_file_name)
        call(full_command)
        return 1

    #directly shutdown by reboot
    def shutdown_test(self):
        temp_conn = remote_connector(self.server, self.username, self.password)

        temp_conn.send_command(
            'echo %s | sudo -S reboot' % self.password
            )

    def cleanup_test(self):
        temp_conn = remote_connector(self.server, self.username, self.password)

        temp_conn.send_command(
            ('cd ' + self.start_script_path) + 
            ';' + 
            'echo %s | sudo -S ' +
            self.cleanup_script) 
