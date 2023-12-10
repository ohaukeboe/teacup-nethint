# Simple experiment with two tcp flows with two hosts and one
# router
#
# $Id: $

import sys
import datetime
from fabric.api import env


#
# Fabric config
#

# User and password
env.user = 'root'
env.password = 'teacup'

# Set shell used to execute commands
env.shell = '/bin/sh -c'

#
# Testbed config
#

# Path to teacup scripts
#TPCONF_script_path = '/home/teacup/git/teacup'
#TPCONF_script_path = '/home/teacup/kristian/teacup'
# TPCONF_script_path = '/home/teacup/michael/teacup-nd'
TPCONF_script_path = '/home/teacup/oskar/teacup-nd'

TPCONF_bc_ping_enable = '1'

# DO NOT remove the following line
sys.path.append(TPCONF_script_path)

# Set debugging level (0 = no debugging info output)
TPCONF_debug_level = 1

TPCONF_pcap_snaplen = 400

# Host lists
TPCONF_router = ['router', ]
TPCONF_hosts = ['pc01', 'pc02', 'pc03', 'pc04', 'pc05']

# Map external IPs to internal IPs
# Wired
# TPCONF_host_internal_ip = {
#     'router': ['172.16.10.254', '172.16.11.254', '172.16.12.254'],
#     'pc01':  ['10.10.12.1'],
#     'pc02':  ['10.10.12.2', '172.16.10.2'],
#     'pc03':  ['172.16.11.3'],
#     'pc04':  ['172.16.12.4'],
#     'pc05':  ['172.16.12.5'],
# }

# Wireless
TPCONF_host_internal_ip = {
    'router': ['172.16.10.254', '172.16.11.254', '172.16.12.254',],
    'pc01':  ['10.10.12.1'],
    'pc02':  ['10.10.12.2', '172.16.10.2'],
    'pc03':  ['172.16.11.3'],
    'pc04':  ['172.16.13.3'],
    'pc05':  ['172.16.13.4'],
}

filename = 'subconfig.py'
with open(filename) as file:
    exec(file.read())
