import paramiko
from scp import SCPClient
import shutil
import utility.remote_connector as rc


class data_downloader:

    def __init__(self, IP = None, uname = None, password = None, test_info_path = None, test_info_name = None, cfg = None):
        if cfg is None:
            self.server = IP
            self.username = uname
            self.password = password
            self.test_folder_info_path = test_info_path
            self.test_folder_info_name = test_info_name
            self.temp_connector = rc.remote_connector(self.server, self.username, self.password)
        else:
            self.server = cfg.server
            self.username = cfg.username
            self.password = cfg.password
            self.test_folder_info_path = cfg.test_folder_info_path
            self.test_folder_info_name = cfg.test_folder_info_name
            self.temp_connector = rc.remote_connector(cfg.server, cfg.username, cfg.password)

        self.cfg = cfg


    def get_current_test_name(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = self.server, username = self.username, password = self.password)
        scp = SCPClient(ssh.get_transport())

        stdin, stdout, stderr = ssh.exec_command('cat %s' % (self.test_folder_info_path + self.test_folder_info_name))
        for out in stdout:
            test_folder_name = out.rstrip()

        scp.close()
        ssh.close()
        return test_folder_name


    def download_data(self, data_path, dest_path, is_folder, is_all_subfile, local_path):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = self.server, username = self.username, password = self.password)
        scp = SCPClient(ssh.get_transport())

        ret_dest_path = ''
        if(is_all_subfile):
            stdin, stdout, stderr = ssh.exec_command('ls %s' % data_path)
            for out in stdout:
                temp_out = out.rstrip()
                scp.get((data_path + temp_out), local_path = (dest_path + local_path))
                ret_dest_path = local_path
        else: 
            scp.get(data_path, local_path = dest_path, recursive = is_folder)

        scp.close()
        ssh.close()

        return 1

    def run_download_pre_processor(self):
        temp_script_path = self.cfg.download_pre_processor
        print (self.temp_connector.send_command(temp_script_path, True))
        

    def download_apache_log(self, dest_path, test_folder_name):
        apache_log_path = '/var/log/tomcat7/'
        self.download_data(apache_log_path, dest_path, True, True, test_folder_name)
        return 1
  
    def download_counter_log(self, dest_path):
        cur_test_path = self.get_current_test_name()
        data_path = self.test_folder_info_path + cur_test_path
        print(data_path)

        self.download_data(data_path, dest_path, True, False, '')
        return (dest_path + cur_test_path)

    
    def collect_result(self, jmeter_result_name):
        self.run_download_pre_processor()

        self.download_counter_log(self.cfg.test_dest_folder)
        cur_test_name = self.get_current_test_name()
        self.download_apache_log(self.cfg.test_dest_folder, cur_test_name)
        self.cur_datafolder_path = self.cfg.test_dest_folder + cur_test_name + "/"
        shutil.move(jmeter_result_name, self.cur_datafolder_path)
        return True
