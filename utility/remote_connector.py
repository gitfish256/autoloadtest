import paramiko
import os
import time
import re

class remote_connector(object):
    """description of class"""

    sslport = 22

    def __init__(self, IP = None, uname = None, password = None, cfg = None):
        if cfg is None:
            self.server = IP
            self.username = uname
            self.password = password
        else:
            self.server = cfg.server
            self.username = cfg.username
            self.password = cfg.password
           
 
    def send_command(self, command, is_sudo = False, is_close = True):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = self.server, port = self.sslport, username = self.username, password = self.password)


        if is_sudo:
            sudo_str = ('echo %s | sudo -S ' + command) % self.password
            #sudo_str = re.sub("(\u2018|\u2019)", "", sudo_str)

            stdin, stdout, stderr = ssh.exec_command(sudo_str)
        else:
            stdin, stdout, stderr = ssh.exec_command(command)

 
        
        ret_list = []
        for out in stdout:
            ret_list.append(out.rstrip())

        for err in stderr:
            ret_list.append(err.rstrip())
        
        if is_close is True:
            ssh.close()

        print "done " + command

        
        return ret_list


    '''
        For now just use sleep, cuz some times ping is not stable
    '''
    def check_online(self, time_out, is_reboot = True):
        print("check/sleep")

        wait_time = time_out/1000
        time.sleep(wait_time)
        return True
        
        temp_iter = 0
        
        while temp_iter < wait_time:
            ret = os.system("ping -w 1000 " + self.server)
            temp_iter += 1
            if ret is 0:
                return True

        raise SystemError("SUT down")
        return False

    
    
