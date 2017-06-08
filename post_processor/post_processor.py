import utility as util
import utility.remote_connector as rc
import config.config_reader as cr
import plan_encoder.jmeter_encoder as jmeter_encoder


class post_processor(object):
    """description of class"""

    def __init__(self, cfg, cur_run_row):
        self.cfg = cfg
        self.temp_connector = rc.remote_connector(self.cfg.server, self.cfg.username, self.cfg.password)
        self.cur_run_info = cur_run_row
        self.output_plan_name = None
        self.read_run_name = None
        self.total_duration = None
        self.temp_encoder = None

    def run_post_script(self):
        post_script_path = self.cur_run_info['post_script']
        print (self.temp_connector.send_command(post_script_path, True))
