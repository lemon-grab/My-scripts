#! /usr/bin/env python3

import subprocess
import optparse
import re
from termcolor import colored


# Banner
Banner = ('''
 _                                      ____           _     
| |    ___ _ __ ___   ___  _ __        / ___|_ __ __ _| |__  
| |   / _ \ '_ ` _ \ / _ \| '_ \ _____| |  _| '__/ _` | '_ \ 
| |__|  __/ | | | | | (_) | | | |_____| |_| | | | (_| | |_) |
|_____\___|_| |_| |_|\___/|_| |_|      \____|_|  \__,_|_.__/ 

''')
print(colored('--------------------------------------------------------------------' , 'yellow'))
print(colored(Banner , 'red'))
print(colored('--------------------------------------------------------------------' , 'yellow'))

#  Our Fonctions

def get_arguments() :
    usage = "macchanger.py -i interface -m new mac"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-i" ,"--interface" ,dest="interface",help="Interface to change its MAC address")
    parser.add_option("-m" ,"--mac" ,dest="new_mac",help="New MAC address")
    (options , arguments) = parser.parse_args()
    if not options.interface :
        parser.error("[-] Please specify the interface , or use --help for more info")
    elif not options.new_mac :
        parser.error("[-] Please specify the Mac address , or use --help for more info")
    return options


def change_mac(interface , new_mac) :
    print(colored("[+]",'green'),"Changing MAC address for",interface)
    subprocess.call(['sudo','ifconfig' ,interface , "down"  ])
    subprocess.call(['sudo','ifconfig' ,interface , "hw","ether" , new_mac ])
    subprocess.call(['sudo','ifconfig' ,interface , "up"])
    

def get_current_mac(interface) :
    ifconfig_result = subprocess.check_output([f"ifconfig",interface])
    search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',str(ifconfig_result))

    if search_result :
        return search_result.group(0)
    else : 
        print(colored("[-]",'red'),"Could not find MAC address for", options.interface)
        exit()


# Executed Code
options = get_arguments()


old_mac = get_current_mac(options.interface)
print(colored("[+]",'green'),"Current" , options.interface , "MAC = " + old_mac)

change_mac(options.interface , options.new_mac)

# Check if the MAC changed or not
current_mac = get_current_mac(options.interface)

if old_mac == current_mac :
    print(colored("[-] MAC address did not change ! Try to run it as root." , 'red'))
else : 
    print(colored("[+] MAC address sucsessfully changed to " ,'green') , colored(options.new_mac , "yellow"))
