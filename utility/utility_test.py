import unittest
import config.config_reader as cfg
import utility as util
import test_list_connector as tl_con
import remote_connector as rc
import multi_connector as mc
import time

class Test_test1(unittest.TestCase):
     
    def __init__(self, methodName = 'runTest'):
       self.temp_cfg = cfg.config_reader("JMS_auto_config.cfg")
       self.rc = rc.remote_connector(self.temp_cfg.server, self.temp_cfg.username, self.temp_cfg.password)

       return super(Test_test1, self).__init__(methodName) 

    def test_set_initial_wl(self):
        temp_util = utility.create_initial_workload_file("MLR", "dspurchase_rpt", 60, 6)

    def test_write_to_snapshot(self):
        utility.write_to_snapshot("aaa", "MLR", "T_.CPU", 4)

    def test_read_from_snapshot(self):
        temp_result = utility.read_from_snapshot("aaa")
        print(temp_result)

    def test_restore_from_snapshot(self):
        temp_result = utility.read_from_snapshot("aaa")

        model_list = ["RegTree", "MLR", "QUANT"]
        deps_list = ["dspurchase_rpt", "T_.CPU", "dsbrowse_rpt", "M_.CPU", "dslogin_rpt",   "dsnewcustomer_rpt"]

        cur_model = temp_result['model_name']
        cur_deps = temp_result['deps_name']
        loop_model_list = model_list[model_list.index(cur_model):]
        loop_deps_list = deps_list[deps_list.index(cur_deps):]
        continue_flag = True

        for temp_model in loop_model_list:
            if continue_flag == True:
                loop_deps_list = deps_list[deps_list.index(cur_deps):]
                continue_flag = False
            else:
                loop_deps_list = deps_list

            for temp_deps in loop_deps_list:
                print(''.join([temp_model, "_", temp_deps]) + "\n")


#        for i, temp_model in enumerate(model_list):

    def test_create_workload_file_name(self):
        temp_result = utility.create_workload_file_name("ttt", "a", "workload", "")
        print(temp_result + "\n")
        temp_result = utility.create_workload_file_name("ttt", "a", "workload", "out")
        print(temp_result + "\n")
    

    '''used to get path from wl file '''
    def test_get_summary(self):
        util.get_summary_list_by_workload_file('workload-SLD_lv5.csv', 'K:\\DS2\\bn_run\\SLD_20kuser_bp_lock', 'tail') 

    def test_get_next_test(self):
        temp = tl_con.test_list_connector("test_list.csv")
        aa = temp.get_next_test()
        print(aa)
        
    def test_send_command(self):
        temp = rc.remote_connector(self.temp_cfg.server, self.temp_cfg.username, self.temp_cfg.password)
        #temp.send_command("reboot", True)
        print(temp.send_command("ls"))
        print(temp.send_command("ls", True))

    def test_clean_script(self):
        temp = rc.remote_connector(self.temp_cfg.server, self.temp_cfg.username, self.temp_cfg.password)
        print(temp.send_command("/home/tes/Desktop/lab/PetClinic/auto_allclean.sh", True))

    def test_check_online(self):
        print(self.rc.check_online(3000))
        print(self.rc.check_online(30000))

    def test_multi_send_cmd(self):
        #print "aa"
        #time.sleep(3600)
        temp_multi_conn = mc.multi_connector([],
                                             [],
                                             [])


        #post process
        temp_multi_conn.send_cmd("python run_sadf.py", 0)

        
        


if __name__ == '__main__':
    unittest.main() 