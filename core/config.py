'''
Copyright (C) 2020 Josh Schiavone - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license, which unfortunately won't be
written for another century.

You should have received a copy of the MIT license with
this file. If not, visit : https://opensource.org/licenses/MIT
'''

import os, sys
import time

import getpass
import platform

import netifaces
from termcolor import cprint, colored

import textwrap

# Console colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray
BOLD = '\033[1m'
END = '\033[0m'

class Config:
    # Program return value handlers
    ESPI_ERROR_CODE_STANDARD = -1
    ESPI_SUCCESS_CODE_STANDARD = 0
    ESPIONAGE_PROCESS_ACTIVE = False

    # Interface Handlers
    ESPI_WLAN0_NET_INTERFACE = 'wlan0'
    ESPI_WLAN1_NET_INTERFACE = 'wlan1'
    ESPI_ETH0_NET_INTERFACE = 'eth0'
    ESPI_ETH1_NET_INTERFACE = 'eth1'

    ESPI_WLAN1_SPECIAL_INTERFACE = 'wlp1s0'
    ESPI_WLAN2_SPECIAL_INTERFACE = 'wlp2s0'
    ESPI_WLAN3_SPECIAL_INTERFACE = 'wlp3s0'

    ESPI_ETH1_SPECIAL_INTERFACE = "enp1s0"
    ESPI_ETH2_SPECIAL_INTERFACE = "enp2s0"
    ESPI_ETH3_SPECIAL_INTERFACE = "enp3s0"

    # Port Handlers
    ESPI_HTTP_DEFAULT_PORT = 80
    
    # OS Handlers
    ESPI_OSYSTEM_UNIX_LINUX = False
    ESPI_OSYSTEM_DARWIN_OSX = False
    ESPI_OSYSTEM_WIN32_64 = False

    # Frame Handlers
    ESPI_ETHERNET_FRAME_STR = "! 6s 6s H"
    ESPI_IPV4_BYTES_STR = "! 8x B B 2x 4s 4s"
    ESPI_ICMP_BYTES_STR = "! B B H"
    ESPI_TCP_SEGMENT_FORMAT = "! H H L L H"
    ESPI_UDP_SEGMENT_FORMAT = "! H H 2x H"
    ESPI_TCP_STRUCT_SEGMENT_FORMAT = "! H H L L H H H H H H"
    # ASCII Handlers
    ESPI_ASCII_DOWN_ARROW = u"\u2193"
    # Shifters
    __version_header_shifter_length__ = 4
    __flag_urg_shift_value__ = 5
    __flag_ack_shift_value__ = 4
    __flag_psh_shift_value__ = 3
    __flag_rst_shift_value__ = 2
    __flag_syn_fin_shift_value__ = 1


class Espionage(object):

    def print_espionage_message(self, msg, color=True):
        espionage = '\n[espionage]>'
        icon = '[*] '
        if color:
            print(BOLD + G + espionage + R + msg + END)
        else: print(icon + msg)

    def print_espionage_notab(self, msg, color=True):
        espionage = '[espionage]>'
        icon = '[*] '
        if color:
            cprint(icon + msg, 'blue', attrs=['bold'])
        else:
            print(f"\t[!] {msg}")

    def print_espionage_noprefix(self, msg, color=True):
        espionage = '[espionage]>'
        if color:
            cprint(msg, 'green', attrs=['bold'])
        else: print('\t' + msg)

    '''
    For functions that provide longer wait times for an output
    '''
    def espionage_animate(self):
        iter_chars = ['|', '/', '-', '\\']
        while end_loader == False:
            for j in itertools.cycle(iter_chars):
                sys.stdout.write("\r\tScyllaProcess - Loading... " + j)
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write("\r\tFinished.")

class Platform(object):

    def GetHostnameDescriptor(self):
        return platform.node()

    def GetUsernameDescriptor(self):
        return getpass.getuser()

    def GetOperatingSystemDescriptor(self):
        e = Espionage()
        p = Platform()
        cfg = Config()

        if sys.platform == "win32" or sys.platform == "win64":
            cfg.ESPI_OSYSTEM_WIN32_64 = True
            e.print_espionage_notab("OS: Windows | (" + p.GetUsernameDescriptor() + '@' +
                p.GetHostnameDescriptor() + ")", color=True)

        if sys.platform == "darwin":
            cfg.ESPI_OSYSTEM_DARWIN_OSX = True
            e.print_espionage_notab("OS: OSX/Darwin | (" + p.GetUsernameDescriptor() + '@' +
                p.GetHostnameDescriptor() + ")", color=True)

        if sys.platform == "linux" or sys.platform == "linux2":
            cfg.ESPI_OSYSTEM_UNIX_LINUX = True
            e.print_espionage_notab("OS: Unix/Linux | (" + p.GetUsernameDescriptor() + '@' +
                p.GetHostnameDescriptor() + ")", color=True)


    def EspionageClear(self):
        time.sleep(0.7)
        if sys.platform == "win32" or sys.platform == "win64":
            os.system("cls")

        if sys.platform == "darwin" or sys.platform == "linux" or sys.platform == "linux2":
            os.system("clear")

class Interface(object):
    def __init__(self, netinterface):
        self.netinterface = netinterface

    def is_interface_up(self):
        iface_addr = netifaces.ifaddresses(self.netinterface)
        return netifaces.AF_INET in iface_addr
            
class PCAP(object):
    def __init__(self, fname):
        self.fname = fname
        
    def write_to_pcap_file(self, stringdata):
        with open(self.fname, 'a') as pcap_file:
            pcap_file.write(stringdata)

def espionage_textwrapper(prefix, string, size=80):
        size -= len(prefix)
        if isinstance(string, bytes):
            string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
            if size % 2:
                size-= 1
                return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])