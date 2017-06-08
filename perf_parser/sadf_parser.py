import pandas
import sys
import re
import subprocess
project_path = sys.path[0] + "\\.."
sys.path.append(project_path)


import data_processor.summary_controller as sc
import os
import fnmatch


class sadf_parser(object):
    """description of class"""
    #timestamp_name = "T_Time"
    timestamp_name = "T_Time"

    header_list = [
        "# hostname;interval;timestamp;CPU;%usr;%nice;%sys;%iowait;%steal;%irq;%soft;%guest;%gnice;%idle",
        "# hostname;interval;timestamp;proc/s;cswch/s",
        "# hostname;interval;timestamp;INTR;intr/s",
        "# hostname;interval;timestamp;pswpin/s;pswpout/s",
        "# hostname;interval;timestamp;pgpgin/s;pgpgout/s;fault/s;majflt/s;pgfree/s;pgscank/s;pgscand/s;pgsteal/s;%vmeff",
        "# hostname;interval;timestamp;tps;rtps;wtps;bread/s;bwrtn/s",
        "# hostname;interval;timestamp;frmpg/s;bufpg/s;campg/s",
        "# hostname;interval;timestamp;kbmemfree;kbmemused;%memused;kbbuffers;kbcached;kbcommit;%commit;kbactive;kbinact;kbdirty",
        "# hostname;interval;timestamp;kbswpfree;kbswpused;%swpused;kbswpcad;%swpcad",
        "# hostname;interval;timestamp;kbhugfree;kbhugused;%hugused",
        "# hostname;interval;timestamp;dentunusd;file-nr;inode-nr;pty-nr",
        "# hostname;interval;timestamp;runq-sz;plist-sz;ldavg-1;ldavg-5;ldavg-15;blocked",
# all 0 line, header has 10 but has 15 columns number
#        "# hostname;interval;timestamp;TTY;rcvin/s;txmtin/s;framerr/s;prtyerr/s;brk/s;ovrun/s",
        "# hostname;interval;timestamp;DEV;tps;rd_sec/s;wr_sec/s;avgrq-sz;avgqu-sz;await;svctm;%util",
        "# hostname;interval;timestamp;IFACE;rxpck/s;txpck/s;rxkB/s;txkB/s;rxcmp/s;txcmp/s;rxmcst/s;%ifutil",
        "# hostname;interval;timestamp;IFACE;rxerr/s;txerr/s;coll/s;rxdrop/s;txdrop/s;txcarr/s;rxfram/s;rxfifo/s;txfifo/s",
        "# hostname;interval;timestamp;call/s;retrans/s;read/s;write/s;access/s;getatt/s",
        "# hostname;interval;timestamp;scall/s;badcall/s;packet/s;udp/s;tcp/s;hit/s;miss/s;sread/s;swrite/s;saccess/s;sgetatt/s",
        "# hostname;interval;timestamp;totsck;tcpsck;udpsck;rawsck;ip-frag;tcp-tw",
        "# hostname;interval;timestamp;irec/s;fwddgm/s;idel/s;orq/s;asmrq/s;asmok/s;fragok/s;fragcrt/s",
        "# hostname;interval;timestamp;ihdrerr/s;iadrerr/s;iukwnpr/s;idisc/s;odisc/s;onort/s;asmf/s;fragf/s",
        "# hostname;interval;timestamp;imsg/s;omsg/s;iech/s;iechr/s;oech/s;oechr/s;itm/s;itmr/s;otm/s;otmr/s;iadrmk/s;iadrmkr/s;oadrmk/s;oadrmkr/s",
        "# hostname;interval;timestamp;ierr/s;oerr/s;idstunr/s;odstunr/s;itmex/s;otmex/s;iparmpb/s;oparmpb/s;isrcq/s;osrcq/s;iredir/s;oredir/s",
        "# hostname;interval;timestamp;active/s;passive/s;iseg/s;oseg/s",
        "# hostname;interval;timestamp;atmptf/s;estres/s;retrans/s;isegerr/s;orsts/s",
        "# hostname;interval;timestamp;idgm/s;odgm/s;noport/s;idgmerr/s",
        "# hostname;interval;timestamp;tcp6sck;udp6sck;raw6sck;ip6-frag",
        "# hostname;interval;timestamp;irec6/s;fwddgm6/s;idel6/s;orq6/s;asmrq6/s;asmok6/s;imcpck6/s;omcpck6/s;fragok6/s;fragcr6/s",
        "# hostname;interval;timestamp;ihdrer6/s;iadrer6/s;iukwnp6/s;i2big6/s;idisc6/s;odisc6/s;inort6/s;onort6/s;asmf6/s;fragf6/s;itrpck6/s",
        "# hostname;interval;timestamp;imsg6/s;omsg6/s;iech6/s;iechr6/s;oechr6/s;igmbq6/s;igmbr6/s;ogmbr6/s;igmbrd6/s;ogmbrd6/s;irtsol6/s;ortsol6/s;irtad6/s;inbsol6/s;onbsol6/s;inbad6/s;onbad6/s",
        "# hostname;interval;timestamp;ierr6/s;idtunr6/s;odtunr6/s;itmex6/s;otmex6/s;iprmpb6/s;oprmpb6/s;iredir6/s;oredir6/s;ipck2b6/s;opck2b6/s",
        "# hostname;interval;timestamp;idgm6/s;odgm6/s;noport6/s;idgmer6/s"]


    def __init__(self, sadf_file_in, target_interval, sig_name):
        self.filter_sig_list = {'CPU':'-1', 'INTR':'-1', 'DEV':'dev8-0', 'IFACE':'eth0'}
        self.parse_header_file = "perf_parser\\parse_list"
        self.unused_column_list = ["# hostname", "interval"]
        self.sadf_file_in = sadf_file_in
        self.sadf_file_handle = open(sadf_file_in, 'r')
        self.sadf_info = self.sadf_file_handle.readlines()
        self.default_delimiter = ';'
        self.target_interval = target_interval
        self.sig_name = sig_name
        

    def get_sub_df(self, header):
        ret_list = []

        iter_start = self.sadf_info.index(header + '\n')
        
        for temp_line in self.sadf_info[iter_start + 1:]:
            if temp_line.startswith('#'):
                break
            ret_list.append(temp_line.rstrip().split(';'))

        ret_df = pandas.DataFrame(ret_list, columns = header.split(';'))
        return ret_df


    def get_cpu_df(self):
        ret_df = self.get_sub_df(self.header_list[0])
        return ret_df

    def get_per_core_stats(self):
        all_cpu_df = self.get_cpu_df()

        core0_df = self.clear_unused_column(self.filter_sub_df(all_cpu_df, {'CPU':'0'}))
        core1_df = self.clear_unused_column(self.filter_sub_df(all_cpu_df, {'CPU':'1'}))
       
        merged_df = pandas.merge(core0_df, core1_df, how = 'inner', on = 'timestamp', suffixes = ['_0', '_1'])

        return merged_df
   

    def get_core_series_by_suffix(self, input_line, suffix, output_suffix):
        temp_header = input_line.index.tolist()
        ret_header = [i for i in temp_header if re.search(suffix, i)]

        ret_series = input_line[ret_header]
        core_header = [x.replace(suffix, output_suffix) for x in ret_header]

        ret_series.index = core_header
        return ret_series
         

    def get_core_mapping_df(self, sadf_df, sum_core_header, sum_suffix):

        df_out = pandas.DataFrame()
        
        for index, temp_line in sadf_df.iterrows():
            target_core = temp_line[sum_core_header]
            if target_core == temp_line['CPU_0']:
                ret_series = self.get_core_series_by_suffix(temp_line, '_0', sum_suffix)
            elif target_core == temp_line['CPU_1']:
                ret_series = self.get_core_series_by_suffix(temp_line, '_1', sum_suffix)
            else:
                print 'error in core mapping'

            df_out = df_out.append(ret_series, ignore_index = True)

        df_out.columns = ret_series.index
        return df_out

    def filter_sub_df(self, df_in, filter_sig_list):
        filtered_flag = False

        for key, val in filter_sig_list.iteritems():
            if key in df_in.columns.tolist():
                df_out = df_in[df_in[key] == val]
                filtered_flag = True
        
        if not filtered_flag:
            df_out = df_in

        return df_out


    def clear_unused_column(self, df_in):

        df_out = df_in
        for temp_drop in self.unused_column_list:
            df_out = df_out.drop(temp_drop, 1)
        
        return df_out
        
    
    def get_filtered_df_by_header(self, header):
        temp_df = self.get_sub_df(header)
        temp_df = self.filter_sub_df(temp_df, self.filter_sig_list)
        temp_df = self.clear_unused_column(temp_df)

        return temp_df


    def scale_df_by_time(self, lower_time, upper_time, df_in):
        temp_df = df_in[(df_in['timestamp'] > lower_time) & (df_in['timestamp'] <= upper_time)]
        #list_out = [pandas.DataFrame.mean(column) for column in temp_df]
        series_out = pandas.DataFrame.mean(temp_df)
        series_out['timestamp'] = upper_time
        return series_out


    def covert_df_to_float(self, df_in):
        df_out = df_in.apply(lambda f : pandas.to_numeric(f, errors='coerce'))
        df_out = df_out.dropna(axis = 1)
        return (df_out)


    def scale_df_by_timestamp(self, timestamp_list, df_in, interval_in):  
        df_out = pandas.DataFrame()

        temp_upper_time = timestamp_list[0]
        temp_lower_time = timestamp_list[0] - interval_in
        temp_out = self.scale_df_by_time(temp_lower_time, temp_upper_time, df_in)
        df_out = df_out.append(temp_out, ignore_index = True)

        index = 1
        for temp_time in timestamp_list[index:]:
            temp_lower_time = timestamp_list[index - 1]
            temp_upper_time = timestamp_list[index]
            temp_out = self.scale_df_by_time(temp_lower_time, temp_upper_time, df_in)
            df_out = df_out.append(temp_out, ignore_index = True)
            index += 1

        return df_out


    def merge_to_summary(self, sum_name_in, df_in):
        temp_sum = pandas.read_csv(sum_name_in)
        
        df_rename = df_in.rename(columns = {'timestamp':self.timestamp_name})
        df_out = pandas.merge(temp_sum, df_rename, how = 'inner', on = self.timestamp_name)
        return df_out

    def if_over_threshold(self, core_df_in):
        new_col = core_df_in.filter(regex = "%idle_\w")
        temp_col_name = new_col.columns.tolist()
        new_header = [re.sub("%idle", "ifover", temp_col_name[0])]

        #see if 100 - idle time larger than 50% with 95% conf interval
        new_content = ((100 - new_col) >= 50 * 0.95)
        new_content.columns = new_header

        return new_content


    def scale_by_CalTime(self, sum_name_in, org_interval, target_interval):
        replace_string = self.sig_name + "_"
        sum_name_out = sum_name_in.replace(replace_string + org_interval, replace_string + str(target_interval))
        R_result = subprocess.Popen(["Rscript", 
                            'CalTime.R', 
                            sum_name_in, 
                            str(target_interval),
                            sum_name_out],
                            stdout=subprocess.PIPE)#,
                           # cwd = self.Rscript_cwd)

        out, err = R_result.communicate()

    def remove_na(self, merge_df):
        merge_df = pandas.DataFrame.dropna(merge_df)
        merge_df = merge_df.reset_index(drop = True)

        return merge_df


def main(folder_in):
    os.chdir(folder_in)
    sadf_name = ''
    sum_name = ''
    target_interval = str(5)
    sig_name = "L1"  

    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, 'sadf*'):
            sadf_name = file
        if fnmatch.fnmatch(file, '*-' + sig_name + '_' + target_interval + '.csv'):
            sum_name = file

    print sadf_name
    print sum_name
    num_name = sum_name.replace("-" + sig_name + "_" + target_interval, "-num_all_" + sig_name + "_" + target_interval)
    thres_name = sum_name.replace("-" + sig_name + "_" + target_interval, "-thres_all_" + sig_name + "_" + target_interval)
    default_name = sum_name.replace("-" + sig_name + "_" + target_interval, "-default_all_" + sig_name + "_" + target_interval)
    all_name = sum_name.replace("-" + sig_name + "_" + target_interval, "-opt23_all_" + sig_name + "_" + target_interval)
    core_name = sum_name.replace("-" + sig_name + "_" + target_interval, "-core_all_" + sig_name + "_" + target_interval)
    map_name = sum_name.replace("-" + sig_name + "_" + target_interval, "-map_all_" + sig_name + "_" + target_interval)

    temp_sadf = sadf_parser(sadf_name, target_interval, sig_name)


    all_df = temp_sadf.get_filtered_df_by_header(temp_sadf.header_list[0])
    for temp_header in temp_sadf.header_list[1:]:
        temp_df = temp_sadf.get_filtered_df_by_header(temp_header)
        all_df = pandas.merge(all_df, temp_df, how = 'inner', on = 'timestamp')

     
    #get per core stats
    per_core_df = temp_sadf.get_per_core_stats()
    all_df = pandas.merge(all_df, per_core_df, how = 'inner', on = 'timestamp') 
    all_df = temp_sadf.covert_df_to_float(all_df)

    #get sum and merge to sum based on sum's timestamp
    test_sum = sc.summary_controller(sum_name)
    temp_timelist = test_sum.get_timestamp()
    scaled_df = temp_sadf.scale_df_by_timestamp(temp_timelist, all_df, int(target_interval))
    merge_df = temp_sadf.merge_to_summary(sum_name, scaled_df)
    
    #remove columns containing NaN (produced when align sar and pidstat logs)
    merge_df = temp_sadf.remove_na(merge_df)

    merge_df.to_csv(default_name, index = False)

    temp_merge_df = merge_df

    '''
    #get core threshold 
    T_core_thres = temp_sadf.if_over_threshold(T_core_df)
    M_core_thres = temp_sadf.if_over_threshold(M_core_df)
    temp_merge_df = temp_merge_df.join(T_core_thres)
    temp_merge_df = temp_merge_df.join(M_core_thres)
    temp_merge_df.to_csv(thres_name, index = False)

    '''

    #test: merge pidstat with per core as training
    per_core_df = temp_sadf.covert_df_to_float(per_core_df)
    scaled_with_core = temp_sadf.scale_df_by_timestamp(temp_timelist, per_core_df, int(target_interval))
    scaled_with_core = temp_sadf.merge_to_summary(sum_name, scaled_with_core)

    scaled_with_core = temp_sadf.remove_na(scaled_with_core)
    scaled_with_core.to_csv(core_name, index = False)

    #get core mapping 
    T_core_df = temp_sadf.get_core_mapping_df(merge_df, 'T_CPU', '_T')
    M_core_df = temp_sadf.get_core_mapping_df(merge_df, 'M_CPU', '_M')

    #output df
    merge_df = merge_df.join(T_core_df)
    merge_df = merge_df.join(M_core_df)
    merge_df = temp_sadf.remove_na(merge_df)

    merge_df.to_csv(num_name, index = False)



    
    #save one containing all columes to check
    temp_merge_df = temp_merge_df.join(T_core_df)
    temp_merge_df = temp_merge_df.join(M_core_df)

    temp_merge_df = temp_sadf.remove_na(temp_merge_df)
    temp_merge_df.to_csv(all_name, index = False)
    
    temp_sadf.scale_by_CalTime(num_name, target_interval, 60)
    temp_sadf.scale_by_CalTime(default_name, target_interval, 60)
    temp_sadf.scale_by_CalTime(core_name, target_interval, 60)




if __name__ == '__main__':
    main(sys.argv[1])

 