import unittest
#import utility.remote_connector as connector
import logging
import sys
#import utility.workload_info_connector as wlcon
import numpy
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utility.remote_connector as connector

import controller.main_controller as cmain
import controller.SLD_evaluation as SLD
import controller.test_list_runner as tlr


class Test_test1(unittest.TestCase):
    server = ''
    username = ''
    password = ''
#    temp_tlr = tlr.test_list_runner("DS2_config.cfg")

    @unittest.skip("skip dup test")
    def test_send_command(self):
        temp_remote = connector.remote_connector(self.server, self.username, self.password)
#        log = logging.getLogger('aaa')
        
        output = temp_remote.send_command('pwd')
#        log.debug(output)
#        self.assertEqual(1, 2, msg = '{0}'.format(output))
        self.assertEqual(output, [u'/home/tes'])


    def test_get_date(self):
        temp_remote = connector.remote_connector(self.server, self.username, self.password)
        output = temp_remote.send_command('date')
        print(output)

    def test_get_predict_result(self):
        temp_ouro = cmain.main_controller("DS2_config.cfg")
        temp_ouro.input_workload_file_name = "pld.csv"
#    def write_predict_result(self, train_data, test_data, model, deps, total_population):
        temp_ouro.write_predict_result("log_02_15_16_RegTree_dspurchase_rpt1caled_summary_60_test_tail.csv",
                                       "log_02_15_16_RegTree_dspurchase_rpt2caled_summary_60_test_tail.csv",
                                       "MLR",
                                       "dspurchase_rpt",
                                       100,
                                       500)

    def test_wlcon(self):
        temp = wlcon.workload_info_connector("pld.csv")
        fa_data = numpy.repeat(222, len(temp.workload_info_header)).tolist()
        fa_data = ["TEST", 100, 0.25, 0.25, 0.25, 0.25, "unchecked", -1, -1, -1]
        temp.write_line_to_data(fa_data)
        temp.write_value(0, "status", "yooo")
        temp.save_to_file()

    
    def test_write_predict_result(self):
        temp_controller = cmain.main_controller("DS2_config.cfg")



    def test_generate_prediction_list(self):
        temp_SLD = SLD.SLD_evaluation()
        temp_df = temp_SLD.generate_prediction_list()
        temp_SLD.save_prediction_list(temp_df, "SLD_prediction.csv")
    
    def test_predict_all_in_file(self):
        temp = SLD.SLD_evaluation()
        temp.partition_run_predict_in_file_by_info("dspurchase_rpt", "MARS",  "path_workload-SLD_lv5.csv")

    def test_partition_run_predict_in_file_by_info(self):
        temp_SLD = SLD.SLD_evaluation()
        temp_SLD.partition_run_predict_in_file_by_info("T_.CPU", 
                                                         "MARS", 
                                                         "temp_path_out.csv", 
                                                         "tc.csv", 
                                                         "to.csv", 
                                                         2)
    def test_get_agg_cm_result_by_key(self):
        temp_sld = SLD.SLD_evaluation()
    
        temp_sld.get_agg_cm_result_by_key("DS2/SLD_result/", "", "MARS")



    def test_pre_process(self):
        temp = tlr.test_list_runner("DS2_config.cfg", "test_list.csv")
        temp.run_pre_process()

    def test_run_test(self):
        self.temp_tlr.run_test()

    def test_clean_system(self):
        test_runner = tlr.test_list_runner("PET_testlist_RQ6.csv")
        test_runner.post_processor.cur_run_info['post_script'] = "/home/tes/Desktop/lab/PetClinic/auto_allclean.sh"
        test_runner.clean_system()


if __name__ == '__main__':
#    logging.basicConfig(stream = unittest.) 
#    logging.getLogger('aaa').setLevel(logging.DEBUG)
    unittest.main()
