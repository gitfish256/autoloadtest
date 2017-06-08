#from rpy2.robjects.packages import STAP
import subprocess
import re
import workload_info_connector as wl_con
import pandas
import os
import glob

def create_initial_workload_file(model_name, deps_in, total_population, indeps_count):
#    file_name = ''.join(['workload', '-', model_name, '-', deps_in, '.csv'])
    file_name = create_workload_file_name(model_name, deps_in, 'workload', "")
    if os.path.isfile(file_name):
        os.remove(file_name)
    temp_data = wl_con.workload_info_connector(file_name)
    temp_series = pandas.Series(data = None, index = temp_data.workload_info_header)
    wl_mix_per_indeps = 1.0 / indeps_count 
    temp_series.loc['model_info'] = 'BEGIN'
    temp_series.loc['total_population'] = total_population
    temp_series.loc['status'] = 'unchecked'
    temp_series.loc[temp_data.workload_mix] = wl_mix_per_indeps
    temp_series.loc[temp_data.result_header] = -1
    temp_series.loc[temp_data.predict_header] = -1
    temp_data.append_line_to_data(temp_series)
    temp_data.save_to_file()
    return file_name


def create_workload_file_name(model_name, deps_in, head_name, tail_name):
    file_name = ''.join([head_name, '-' , model_name, '-', deps_in, tail_name, '.csv'])
    return file_name

def combine_training_data(checked_data_path, unchecked_data_path, output_data_path):
    df1 = pandas.read_csv(checked_data_path)
    df2 = pandas.read_csv(unchecked_data_path)
    
    dfm = pandas.concat([df1, df2])
  
    dfm.to_csv(output_data_path, index = False)

def combine_summary_data(summary_data_path_list, output_data_path):
    df = pandas.read_csv(summary_data_path_list[0])

    for i in summary_data_path_list[1:len(summary_data_path_list)]:
        temp_df = pandas.read_csv(unchecked_data_path)
        df = pandas.concat([df, temp_df])
  
    dfm.to_csv(output_data_path, index = False)
    return output_data_path

def get_summary_path_by_tail(data_foler_in, tail_name):
    data = os.listdir(data_foler_in)
    file_ret = glob.glob(data_foler_in + '*' + '_' + tail_name + '.csv')
    if len(file_ret) > 1:
        print("dup get_summary_path_by_tail")
    return file_ret[0]

def get_summary_list_by_workload_file(workload_file_in, output_file_name, data_path_in, tail_name):
    wl_file = pandas.read_csv(workload_file_in)
    index_list = wl_file['model_info'].tolist()
        
    data_file_list = os.listdir(data_path_in)
    path_list = []
    for index, item in enumerate(index_list):
        for i in data_file_list:
            #get the folder based on index
            sum_path = data_path_in + '\\' + i + '\\'
            if (i.find(item) != -1) and (os.path.isdir(sum_path)):
                file = get_summary_path_by_tail(sum_path, tail_name)
#                print (file)
                path_list.append(file)
    wl_file['sum_path'] = pandas.Series(path_list)
    print (wl_file)
    wl_file.to_csv(output_file_name, index = False)                

    

def get_default_threshold(deps_name_in):
    threshold_for_rpt = 500
    threshold_for_util = 30

    if re.search('_rpt$', deps_name_in) == None:
        return threshold_for_util
    else:
        return threshold_for_rpt

def write_to_snapshot(file_name, model_name, deps_name, round):
    text_file = open(file_name, "w")
    text_file.write(''.join([model_name, ';', deps_name, ';', str(round)]))
    text_file.close()

def read_from_snapshot(file_name):
    temp_dict = {'model_name': '', 'deps_name': '', 'round': ''}
    if not os.path.exists(file_name):
        return None
    
    with open(file_name, "r") as f:
        info_line = f.readline()

    info_list = info_line.split(';')

    temp_dict['model_name'] = info_list[0]
    temp_dict['deps_name'] = info_list[1]
    temp_dict['round'] = info_list[2]
    f.close()
    return temp_dict
    

#if __name__ == '__main__':
#   print(create_initial_workload_file("MLR", "dspurchase_rpt", 100, 4)) 