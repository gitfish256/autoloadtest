import pandas as ps


class test_list_connector(object):
    """
    header: run_name	
            version_file_path	
            deploy_path	
            pre_script	
            post_script	
            status	
            test_plan_path	
            initial_delay	
            startup_time	
            hold_time	
            shutdown_time
 
    """
    
    
    def __init__(self, test_list_file_name):
        self.cur_row_index = -1
        self.cur_row_info = None
        self.test_list_file_name = test_list_file_name
        if test_list_file_name != None:
            self.test_list_info = ps.read_csv(test_list_file_name)
        else:
            self.test_list_info = None
            return

        self.run_name = self.test_list_info

    def get_next_test(self):
        for index, row in self.test_list_info.iterrows():
            if row.loc['status'] != 'checked':
                row.loc['status'] = 'read'
                self.cur_row_index = index
                self.test_list_info.to_csv(self.test_list_file_name, index = False)
                self.cur_row_info = row
                return row
        
        self.cur_row_info = None
        self.cur_row_index = -1
        return None

    def save_to_file(self, file_name = None):
        if file_name is None:
            self.test_list_info.to_csv(self.test_list_file_name, index = False)
        else:
            self.test_list_info.to_csv(file_name, index = False)

        
            
        

