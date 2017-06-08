import ConfigParser as cp
import ast
import key_mng as km

"""
Things to change when changing testing project:
1. cfg file name (no need for new version)
2. setup scripts (no need for new version)
    a. run_sadf.py: os.chdir
3. change db pass if switching between DS2 PET


"""
class config_reader:
    """description of class"""

    cfg_file_name = "DS2_auto_config.cfg"


#    def __init__(self, config_file_path):
    def __init__(self, cfg_file_name = None):
        temp_cfg = cp.ConfigParser()
        #temp_km = km.key_mng("1qaz2wsx1qaz2wsx")

        if cfg_file_name is None:
            temp_cfg.read(self.cfg_file_name)
        else:
            temp_cfg.read(cfg_file_name)



        self.cfg_file = temp_cfg
        temp_group_string = temp_cfg.get("target_system_info", "scenarios")
        

        self.group_name_vec = self.read_string_to_list(temp_group_string, ',')
        self.workload_lengh = len(self.group_name_vec)

        self.deps_all = self.read_string_to_list(temp_cfg.get("target_system_info", "deps_all"), ',')

        self.total_population = int(temp_cfg.get("target_system_info", "total_population"))

        self.is_script_deployment = ast.literal_eval(temp_cfg.get("target_system_info", "script_deployment"))
        self.is_manual_start = ast.literal_eval(temp_cfg.get("target_system_info", "manual_start"))

        #test config
        ## server side
        self.server = temp_cfg.get("server_config", "server_ip")
        self.username = temp_cfg.get("server_config", "username")
        self.password = temp_cfg.get("server_config", "password")
        #self.password = temp_km.decrypt_val(self.password)
        self.start_script_path = temp_cfg.get("server_config", "start_script_path")
        self.start_script_name = temp_cfg.get("server_config", "start_script_name")
        self.start_monitor_only_script_name = temp_cfg.get("server_config", "start_monitor_only_script_name")
        self.test_folder_info_path = temp_cfg.get("server_config", "test_folder_info_path")
        self.test_folder_info_name = temp_cfg.get("server_config", "test_folder_info_name")
        self.monitor_pid_info_file_name = temp_cfg.get("server_config", "monitor_pid_info_file_name")
        self.clean_script_name = temp_cfg.get("server_config", "test_folder_info_name")

        #print "inin"
        ## node side
        self.is_multi_mode = False
        if (temp_cfg.has_section("node_config")):
            #print "in"
            self.is_multi_mode = ast.literal_eval(temp_cfg.get("node_config", "is_multi_mode"))
            self.node_ip_list = self.read_string_to_list(temp_cfg.get("node_config", "node_ip"), ",")
            self.node_user_list = self.read_string_to_list(temp_cfg.get("node_config", "user_list"), ",")
            self.pass_list = self.read_string_to_list(temp_cfg.get("node_config", "pass_list"), ",")
            

        ## test plan side
        self.empty_plan_name = temp_cfg.get("test_plan_config", "empty_plan_name")
        self.wm_plan_name = temp_cfg.get("test_plan_config", "wm_plan_name")
        self.output_plan_name = temp_cfg.get("test_plan_config", "output_plan_name")
        self.initial_delay = int(temp_cfg.get("test_plan_config", "initial_delay"))
        self.startup_time = int(temp_cfg.get("test_plan_config", "startup_time"))
        self.hold_time = int(temp_cfg.get("test_plan_config", "hold_time"))
        self.shutdown_time = int(temp_cfg.get("test_plan_config", "shutdown_time"))
        self.hold_load_file_path = temp_cfg.get("test_plan_config", "hold_load_file_path")
        self.total_duration = int(temp_cfg.get("test_plan_config", "total_duration"))
        self.parse_interval = int(temp_cfg.get("test_plan_config", "parse_interval"))
        self.generator_full_path = temp_cfg.get("test_plan_config", "generator_full_path")
        self.generator_parameter = temp_cfg.get("test_plan_config", "generator_parameter")


        #parsing config
        self.test_dest_folder = temp_cfg.get("parser_config", "test_dest_folder")
        self.parser_script_folder = temp_cfg.get("parser_config", "parser_script_folder")
        self.download_pre_processor = temp_cfg.get("parser_config", "download_pre_processor")
        self.script_start_file_name = temp_cfg.get("parser_config", "script_start_file_name")
        self.summary_tail_name = temp_cfg.get("parser_config", "summary_tail_name")
        self.cut_before = temp_cfg.get("parser_config", "cut_before")
        self.cut_after = temp_cfg.get("parser_config", "cut_after")


        #result analyzer config
        self.Rscript_cwd = temp_cfg.get("result_analyzer_config", "Rscript_cwd")
        self.Roptim_script = temp_cfg.get("result_analyzer_config", "Roptim_script")
        self.RGA_script = temp_cfg.get("result_analyzer_config", "RGA_script")
        self.RD_script = temp_cfg.get("result_analyzer_config", "RD_script")
        
        
    def read_string_to_list(self, string, delimiter):
        temp_string = string.replace(' ', '')
        temp_list = temp_string.split(delimiter)
        return (temp_list)


