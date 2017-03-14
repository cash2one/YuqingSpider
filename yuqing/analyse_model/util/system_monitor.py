# /usr/bin/env python
# -*-coding: utf-8 -*-
__author__ = 'wtq'

import os
import subprocess


def sys_monitor(net_name):
    """
    15分钟内的系统负载
    user、nice、system、irq、softirq五项的使用率相加,综合衡量cpu使用率
    MEM使用量(MB)
    MEM總量(MB)
    指定网卡每秒的平均接收流量 (B/S)
    指定网卡每秒的平均发送流量 (B/S)
    :return:
    """
    node_realtime_info = {}
    p = subprocess.Popen("source /home/wtq/sys_monitor.sh %s" % (net_name), shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
    p.wait()
    sys_out = p.communicate()

    sys_stus = str(sys_out[0]).split("\n")
    # get cpu rate
    cpu_rate = float(sys_stus[1])/float(sys_stus[0])
    node_realtime_info["cpu_rate"] = cpu_rate

    # get mem used
    mem_used = sys_stus[2]
    node_realtime_info["mem_used"] = mem_used

    # get the all disk space and free space
    disk_all_space_raw = sys_stus[3].split("G ")
    disk_free_space = 0
    disk_free_space_raw = sys_stus[4].split("% ")
    disk_use_rate = []
    for j in range(len(disk_free_space_raw)-1):
        disk_use_rate.append(float(disk_free_space_raw[j])/100)
    disk_use_rate.append(float(disk_free_space_raw[-1].split("%")[0])/100)
    disk_all_space = 0
    for j in range(len(disk_all_space_raw)-1):
        disk_all_space += float(disk_all_space_raw[j])
        disk_free_space += float(disk_all_space_raw[j])*disk_use_rate[j]

    disk_free_space += float(disk_all_space_raw[-1].split("G")[0])*disk_use_rate[-1]
    disk_all_space += float(disk_all_space_raw[-1].split("G")[0])

    node_realtime_info["disk_free_space"] = disk_free_space
    node_realtime_info["disk_all_space"] = disk_all_space

    # get network rate
    network_response_rate = sys_stus[5]
    network_request_rate = sys_stus[6]
    node_realtime_info["network_response_rate"] = network_response_rate
    node_realtime_info["network_request_rate"] = network_request_rate

    # get host name and ip
    host_name = os.popen("cat /etc/hostname").read().split("\n")[0]
    ip = os.popen("ifconfig | perl -nle 's/dr:(\S+)/print $1/e'").read().split("\n")
    ip_list = []

    # 这是在获取机器网卡上的所有的IP
    for p in ip:
        if len(p) > 6:
            ip_list.append(p)

    node_realtime_info["node_name"] = host_name
    node_realtime_info["node_ip"] = ip_list

    for key in node_realtime_info:
        print key, node_realtime_info[key]


if __name__ == "__main__":
    sys_monitor('eth0')
