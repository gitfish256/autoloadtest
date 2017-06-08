#from xml.etree.ElementTree import fromstring, ElementTree, Element
import xml.etree.ElementTree as ET
import csv
import random
import sys
import time
from tempfile import NamedTemporaryFile
import shutil
import utility.workload_info_connector as wl_connector
# -*- coding: UTF-8 -*-

class jmeter_encoder:

    def __init__(self):
        self.read_test_name = ""
        return
    '''
        Function takes test plan and sequence of workload mix, output new test plan with the workload mix
        input:
            test plan path
            sequence for utg group
            initial start time
            hold load for
            shutdown time
    '''

    ''' todo: maybe put startup, delay into the file as well'''
    def encode_workload_to_test_plan(self, plan_path, output_plan_name, utg_name_list, thread_list, initial_delay, startup_time, hold_time, shutdown_time):

        temp_initial_delay = initial_delay
        tree = ET.parse(plan_path)
        root = tree.getroot()
        if thread_list == []:
            print "null thread list\n"
            return -1
        hold_load_time_list = []
        for temp_thread_vector in thread_list:
            print(temp_initial_delay)
            res = self.append_schedule_to_plan_root(root, utg_name_list, temp_thread_vector, temp_initial_delay, startup_time, hold_time, shutdown_time)
            hold_load_time_list.append([temp_initial_delay + startup_time, temp_initial_delay + startup_time + hold_time])
            temp_initial_delay = temp_initial_delay + startup_time + hold_time + shutdown_time

            if res == False:
                print "error in encoding"
                return 0
        tree.write(output_plan_name)
    #    print(hold_load_time_list)
        return hold_load_time_list

    def append_schedule_to_plan_root(self, plan_root, utg_name_list, thread_vector, initial_delay, startup_time, hold_time, shutdown_time):

        utg_name_len = len(utg_name_list)
        for temp_utg_index in range(utg_name_len):
            # if the thread count eaquals 0, then skip and encode the next one
            if thread_vector[temp_utg_index] == 0:
                continue
#            print(utg_name_list[temp_utg_index])
            utg_root = plan_root.find('''.//kg.apc.jmeter.threads.UltimateThreadGroup/[@testname='{}']'''.format(utg_name_list[temp_utg_index]))
            self.append_thread_schedule(utg_root, thread_vector[temp_utg_index], initial_delay, startup_time, hold_time, shutdown_time)
        return 1


    def append_thread_schedule(self, utg_root, thread_count, initial_delay, startup_time, hold_time, shutdown_time):

        thread_root = utg_root.find(".//collectionProp/[@name='ultimatethreadgroupdata']")
#        print thread_root

        random_name = random.randint(-sys.maxint, sys.maxint)
        insert_element = ET.fromstring(
        '''        <collectionProp name="{}">
                <stringProp name="{}">{}</stringProp>
                <stringProp name="{}">{}</stringProp>
                <stringProp name="{}">{}</stringProp>
                <stringProp name="{}">{}</stringProp>
                <stringProp name="{}">{}</stringProp>
              </collectionProp>
              '''.format(random_name,
                         thread_count, thread_count,
                         initial_delay, initial_delay,
                         startup_time, startup_time,
                         hold_time, hold_time,
                         shutdown_time, shutdown_time
                        )
        )
        thread_root.append(insert_element)
        return 1


    def parse_workload_to_vec(self, workload_file, workload_names, is_one_by_one):
        temp_data = wl_connector.workload_info_connector(workload_file)
        result_vec_list = []
        temp_workload_name_list = list(workload_names)

        row_index = 0
        total_row = len(temp_data.workload_data)
        temp_workload_name_list.insert(0, "total_population")

        while row_index < total_row:
            temp_row = temp_data.read_line_by_row(row_index)
            if temp_row.loc["status"] == "checked":
                row_index += 1
                continue

            
            thread_mix_info_row = temp_row.loc[temp_workload_name_list].tolist()
            thread_mix_info_row = [float(x) for x in thread_mix_info_row]
            result_vec_list.append(self.workload_mix_to_thread_count(thread_mix_info_row))
            temp_data.write_value(row_index, "status", "read")
            row_index += 1
            self.read_test_name = temp_row["model_info"]

            if is_one_by_one == True:
                break

        temp_data.save_to_file()
        return result_vec_list


    def workload_mix_to_thread_count(self, workload_mix):
        temp_thread_count = [workload_mix[0] * x for x in workload_mix[1:]]
#        print temp_thread_count
#        print [round(x) for x in temp_thread_count]

        return [int(round(x)) for x in temp_thread_count]

    def get_abs_time_for_timeslots(self, hold_load_time_list):
        i = 0
        temp_time = int(time.time()) 
        while i < len(hold_load_time_list):
            j = 0
            while j < len(hold_load_time_list[i]):
                hold_load_time_list[i][j] += temp_time
                j += 1
            i += 1
        return hold_load_time_list

    def get_total_duration(self, hold_load_time_list, shutdown_time):
        return(hold_load_time_list[-1][1] + shutdown_time)
    # test = 1
    #
    # if (test):
    #
    #     workload_vec = parse_workload_to_vec(input_file_name)
    #     encode_workload_to_test_plan(input_plan_name, output_plan_name, group_name_vec, workload_vec, initial_delay, startup_time, hold_time, shutdown_time)

    def write_timeslots_to_file(self, hold_load_time_list, trim_time_file_name, is_abs_time):
        if(is_abs_time == True):
            hold_load_time_list = self.get_abs_time_for_timeslots(hold_load_time_list) 
        f = open(trim_time_file_name, 'w')
        for temp_item in hold_load_time_list:
            for elem in temp_item:
                f.write("%d " % elem)
            f.write("\n")