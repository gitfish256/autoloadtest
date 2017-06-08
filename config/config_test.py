import unittest
import config_reader as cr
import key_mng as km

class Test_test1(unittest.TestCase):

    def test_config_reader(self):
        temp = cr.config_reader()
        print (temp)
        temp2 = cr.config_reader("DS2_auto_config.cfg")
        print (temp2)
        
    def test_km(self):
        temp = km.key_mng("aaa")
        aa = temp.encrypt_val("aaa")
        print(aa)
        print(temp.decrypt_val(aa))

if __name__ == '__main__':
    unittest.main()
