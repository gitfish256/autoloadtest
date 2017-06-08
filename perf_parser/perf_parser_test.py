import unittest
import pandas
import sys

project_path = sys.path[0] + "\\.."
sys.path.append(project_path)
import data_processor.summary_controller as sc
import perf_parser.sadf_parser as sadf_parser


class Test_test1(unittest.TestCase):

    def test_sadf(self):
        folder_name = ""

        sadf_parser.main(folder_name)


    def test_cpu(self):
        sadf_name = "" 
        sum_name = "" 

        merged_name = sum_name.replace("-L1_60", "-testall_L1_60")
        temp_sadf = sadf_parser.sadf_parser(sadf_name)

        temp_sadf.get_per_core_stats()



if __name__ == '__main__':
    unittest.main()
