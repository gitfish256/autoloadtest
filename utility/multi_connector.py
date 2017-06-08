import paramiko
import os
import time
import re
import remote_connector as rc
import datetime

class multi_connector(object):
    """description of class"""

    '''
    IP list should be ordered as reboot sequence
    '''

    def __init__(self, IP_list, user_list, pwd_list):
        
        self.connecter_list = []
        temp_ind = 0
        
        while temp_ind < len(IP_list):
            self.connecter_list.append(rc.remote_connector(IP_list[temp_ind], user_list[temp_ind], pwd_list[temp_ind]))
            temp_ind += 1


    def send_cmd(self, cmd, pause = 0):
        for temp_conn in self.connecter_list:
            print(temp_conn.send_command(cmd, True))
            time.sleep(pause)



        
        




