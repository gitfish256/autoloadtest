#from __future__ import print_function
import unittest
import result_analyzer

class Test_test1(unittest.TestCase):

    def test_get_next_workload(self):
        temp = result_analyzer.result_analyzer("k:\\BnOpti\\MARS_v1_ds2\\", "GA_workload_search.R", 0)
        print(temp.get_next_workload('''k:\BnOpti\HQ_controller\workload-RegTree-T_.CPU.csv''', 100))

        

if __name__ == '__main__':
    unittest.main()
