from ast import And
from sqlite3 import connect
import time
from netmiko import ConnectHandler
from datetime import datetime
from multiprocessing import Queue
import threading
import pathlib
import os
import re


devices_file = open("updated_scan.txt")  ## open the ip list file from root folder
devices_file.seek(0)  ## put the first read on the begining
ip_list = devices_file.read().splitlines()  ## splite the ip's in a list
print(ip_list)
devices_file.close()
initial = 'HP'


def get_info(IP,any):
    switch = {
            'device_type': 'ruckus_fastiron_telnet',
            'ip': IP,
            'password': 'C0r@lSe@',  # telnet Pass
            'secret': 'C0r@lSe@',  # Enable Pas

        }

    connection = ConnectHandler(**switch)
    connection.conn_timeout = 10
    print('Connecting to ' + IP)
    print('-' * 79)
    print('waiting For Authentication ...')
    output = connection.send_command('sh version')
    print(output)
    print()
    print('-' * 79)

    hostname = connection.send_command('show run | i hostname')
    hostname.split(" ")
    if hostname == "":
        device = "no_hostname"
        print('Notice : This switch has no hostname configured')
    else:
        hostname, device = hostname.split(" ")
    print(f'Operating {device}')
    my_ip = IP.strip('\n')

    connection.enable()
    config_commands = [

                        'enable telnet password C0r@lSe@',
                        'enable super-user-password C0r@lSe@',
                        'exit'  ]
    connection.send_config_set(config_commands, delay_factor=4)
    print(f'All passwords on {device} is set..')
    connection.disconnect()
    return




if __name__ == "__main__":
    que = Queue()

    def start():
        threads = []
        for ip in ip_list:
            # Test using sleep delays between devices to wait for writing outputs to text file in order
            try:
                t1 = threading.Thread(target=get_info, args=(ip, que))
                t1.start()
                threads.append(t1)
            except BaseException as e:
                continue
        for t in threads:
            t.join()
            print('Waiting For all switches to finish')

    start()

