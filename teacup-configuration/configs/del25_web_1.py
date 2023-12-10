#
# Experiment settings
#

# Maximum allowed time difference between machines in seconds
# otherwise experiment will abort cause synchronisation problems
TPCONF_max_time_diff = 1

# Experiment name prefix used if not set on the command line
# The command line setting will overrule this config setting
now = datetime.datetime.today()
TPCONF_test_id = now.strftime("%Y%m%d-%H%M%S") + '_singleflow'

# Directory to store log files on remote host
TPCONF_remote_dir = '/tmp/'

# Number of runs for each setting
TPCONF_runs = 1

#
# List of router queues/pipes
#

# Each entry is a tuple. The first value is the queue number and the second value
# is a comma separated list of parameters (see routersetup.py:init_pipe()).
# Queue numbers must be unique.

# Note that variable parameters must be either constants or or variable names
# defined by the experimenter. Variables are evaluated during runtime. Variable
# names must start with a 'V_'. Parameter names can only contain numbes, letter
# (upper and lower case), underscores (_), and hypen/minus (-).

# All variables must be defined in TPCONF_variable_list (see below).

# Note parameters must be configured appropriately for the router OS, e.g. there
# is no CoDel on FreeBSD; otherwise the experiment will abort witn an error.

TPCONF_router_queues = [
    # Set same delay for every host
    ('1', " source='0.0.0.0/0', dest='172.16.12.0/24', delay=V_delay, "
     " loss=V_loss, rate=V_up_rate, queue_disc=V_aqm, queue_size=V_bsize "),
    ('2', " source='172.16.12.0/24', dest='0.0.0.0/0', delay=V_delay, "
     " loss=V_loss, rate=V_down_rate, queue_disc=V_aqm, queue_size=V_bsize "),
]

#
# List of traffic generators
#

# Each entry is a 3-tuple. the first value of the tuple must be a float and is the
# time relative to the start of the experiment when tasks are excuted. If two tasks
# have the same start time their start order is arbitrary. The second entry of the
# tuple is the task number and  must be a unique integer (used as ID for the process).
# The last value of the tuple is a comma separated list of parameters (see the tasks
# defined in trafficgens.py); the first parameter of this list must be the
# task name.

# Client and server can be specified using the external/control IP addresses or host
# names. Then the actual interface used is the _first_ internal address (according to
# TPCONF_host_internal_ip). Alternativly, client and server can be specified as
# internal addresses, which allows to use any internal interfaces configured.

traffic_iperf = [
    # Specifying external addresses traffic will be created using the _first_
    # internal addresses (according to TPCONF_host_internal_ip)
    # pc01 -> pc04
    # Web
    ('0.0', '2', " start_custom_traffic,"
     " name='httperf',"
     " directory='/usr/bin',"
     " duration=V_duration,"
     " hostname='pc04',"
     " parameters='--server 10.10.12.1 --port 80 --rate 90 --num-conns %s' % (V_duration*90)"),

    ('0.0', '1', " start_http_server, server='pc01', port=80 "),

    # pc03 -> pc05
    ('0.0', '5', " start_iperf, client='pc05', server='pc03', port=5001,"
     " duration=V_duration, extra_params_client='-b 16k -l 100 -i 0.05' "),

    # ('0.0', '3', " start_iperf, client='pc01', server='pc04', port=5003,"
    #  " duration=V_duration, extra_params_client='-b 16k -l 100 -i 0.05' "),
    # ('0.0', '4', " start_iperf, client='pc03', server='pc05', port=5001,"
    #  " duration=V_duration "),



    # ('0.0', '1', " start_custom_traffic,"
    #  " name='python3',"
    #  " directory='/usr/bin',"
    #  " hostname='pc01',"
    #  " duration=V_duration,"
    #  " parameters='-m http.server 80'"),

    # ('0.0', '11', " create_http_incast_content, server='pc01', duration=2*V_duration, "),
    #  #" sizes=V_inc_content_sizes_str "),


    # ('0.0', '3', " create_http_incast_content, server='pc01', duration=2*V_duration, "),
    #  # " sizes=V_inc_content_sizes_str "),

    # to use the router as a sender:
    #('0.0', '1', " start_iperf, client='router', server='pc05', port=5001,"
    # " duration=V_duration, extra_params_client='-B 172.16.10.254' "),
    #
    #('0.0', '2', " start_iperf, client='testhost2', server='testhost1', port=5001, "
    # " duration=V_duration "),
    # Or using internal addresses
    # ( '0.0', '1', " start_iperf, client='172.16.11.2', server='172.16.10.2', "
    #              " port=5000, duration=V_duration " ),
    # ( '0.0', '2', " start_iperf, client='172.16.11.2', server='172.16.10.2', "
    #              " port=5001, duration=V_duration " ),
]

TPCONF_inc_content_sizes = [256]
TPCONF_inc_content_sizes_str = ','.join(
    str(x) for x in TPCONF_inc_content_sizes)

# traffic_ns3 = [
#     ('0.0', '1', " start_custom_traffic,"
#      " name='ncat',"
#      " directory='/bin',"
#      " hostname='testhost1',"
#      " duration=V_duration,"
#      " parameters='-k -l 4444'"),
#     ('2.0', '2', " start_custom_traffic,"
#      " name='wafrun.sh',"
#      " directory='/mnt/ns3/ns-allinone-3.27/ns-3.27',"
#      " hostname='testhost4',"
#      " duration=V_duration,"
#      " parameters='scratch/emu-mux_--teb=1_--initcwnd=10'"),
# ]

# traffic_custom = [
#    ('0.0', '1', " start_custom_traffic,"
#     " name='neat_server',"
#     " directory='/usr/home/teacup/neat/neat-performance/build',"
#     " hostname='testhost1',"
#     " duration=V_duration,"
#     " parameters='-l %s -M %s -p %s -v %s -u %s' % (V_data_size, V_transports, 3323, 0, 2)"),
#    ('2.0', '2', " start_custom_traffic,"
#     " name='neat_client',"
#     " directory='/usr/home/teacup/neat/neat-performance/build',"
#     " hostname='testhost3',"
#     " duration=V_duration,"
#     " parameters='-l %s -M %s -n %s -v %s -u %s %s %s' % (10240, V_transports, V_flows, 0, 2, '172.16.10.1', 3323)"),
# ]

# THIS is the traffic generator setup we will use
#TPCONF_traffic_gens = traffic_iperf

#
# Traffic parameters
#

# Duration in seconds of traffic
TPCONF_duration = 300

# TCP congestion control algorithm used
# Possible algos are: default, host<N>, newreno, cubic, cdg, hd, htcp, compound, vegas
# Note that the algo support is OS specific, so must ensure the right OS is booted
# Windows: newreno (default), compound
# FreeBSD: newreno (default), cubic, hd, htcp, cdg, vegas
# Linux: newreno, cubic (default), htcp, vegas
# Mac: newreno
# If you specify 'default' the default algorithm depending on the OS will be used
# If you specify 'host<N>' where <N> is an integer starting from 0 to then the
# algorithm will be the N-th algorithm specified for the host in TPCONF_host_TCP_algos
# (in case <N> is larger then the number of algorithms specified, it is set to 0
#TPCONF_TCP_algos = ['newreno', 'cubic', ]

TPCONF_TCP_algos = ['newreno', ]

# Specify TCP congestion control algorithms used on each host
TPCONF_host_TCP_algos = {
}

# Specify TCP parameters for each host and each TCP congestion control algorithm
# Each parameter is of the form <sysctl name> = <value> where <value> can be a constant
# or a V_ variable
TPCONF_host_TCP_algo_params = {
}

# Specify arbitray commands that are executed on a host at the end of the host
# intialisation (after general host setup, ecn and tcp setup). The commands are
# executed in the shell as written after any V_ variables have been replaced.
# LIMITATION: only one V_ variable per command
#TPCONF_host_init_custom_cmds = {
#}

tc_delay = '10ms'
tc_rate = '45Mbit'
tc_bsize = '56250'

TPCONF_host_init_custom_cmds = {
   'pc02' : ['tc qdisc del dev enp13s1 root',
             'tc qdisc add dev enp13s1 root handle 2: netem delay %s' % tc_delay,
             'tc qdisc add dev enp13s1 parent 2: handle 3: htb default 10',
             'tc class add dev enp13s1 parent 3: classid 10 htb rate %s' % tc_rate,
             'tc qdisc add dev enp13s1 parent 3:10 handle 11: bfifo limit %s' % tc_bsize],
}

################# custom traffic ################
#traffic_custom = [
#    ('0.0', '1', " start_custom_traffic,"
#     " name='neat_server',"
#     " directory='/usr/home/teacup/neat/neat-performance/build',"
#     " hostname='testhost1',"
#     " duration=V_duration,"
#     " parameters='-l %s -M %s -p %s -v %s -u %s' % (V_data_size, V_transports, 3323, 0, 2)"),
#    ('2.0', '2', " start_custom_traffic,"
#     " name='neat_client',"
#     " directory='/usr/home/teacup/neat/neat-performance/build',"
#     " hostname='testhost2',"
#     " duration=V_duration,"
#     " parameters='-l %s -M %s -n %s -v %s -u %s %s %s' % (10240, V_transports, V_flows, 0, 2, '172.16.10.1', 3323)"),
#]

TPCONF_traffic_gens = traffic_iperf
#TPCONF_traffic_gens = traffic_ns3

# cwnd-poll parameters: source ip address; destination ip address; duration; port
TPCONF_custom_loggers = [
    ('0', " start_custom_logger,"
     " name='cwnd-poll.sh',"
     " logname='cwnd',"
     " directory='/home/teacup',"
     " hostname='pc04',"
     " parameters='172.16.12.4 10.10.12.1 10000000 80'"),
    ('1', " start_custom_logger,"
     " name='cwnd-poll.sh',"
     " logname='cwnd',"
     " directory='/home/teacup',"
     " hostname='pc05',"
     " parameters='172.16.12.5 172.16.11.3 10000000 5001'"),
]

TPCONF_linux_tcp_logger=''

#TPCONF_linux_tcp_logger='ttprobe'
#TPCONF_web10g_poll_interval = 10
#TPCONF_linux_tcp_logger='both'
#TPCONF_ttprobe_output_mode='0'
#TPCONF_ttprobe_direction='io'

#TPCONF_data_sizes = [100000000]

#################################################



# Emulated delays in ms
TPCONF_delays = [25]

# Emulated loss rates
TPCONF_loss_rates = [0]

#TPCONF_flows = [1]
# Emulated bandwidths (downstream, upstream)
TPCONF_bandwidths = [
    ('15mbit', '15mbit'),
    # ('45mbit', '45mbit'),
]

# AQM
# Linux: fifo (mapped to pfifo), pfifo, bfifo, fq_codel, codel, pie, red, ...
#        (see tc man page for full list)
# FreeBSD: fifo, red
#TPCONF_aqms = ['pfifo', 'codel', 'pie', 'red']
TPCONF_aqms = ['pfifo']

# Buffer size
# If router is Linux this is mostly in packets/slots, but it depends on AQM
# (e.g. for bfifo it's bytes)
# If router is FreeBSD this would be in slots by default, but we can specify byte sizes
# (e.g. we can specify 4Kbytes)
# TPCONF_buffer_sizes = [6, 12, 18, 24]
TPCONF_buffer_sizes = [31, 62, 93, 124]
#TPCONF_transports = ['TCP']
#
# List of all parameters that can be varied and default values
#

# The key of each item is the identifier that can be used in TPCONF_vary_parameters
# (see below).
# The value of each item is a 4-tuple. First, a list of variable names.
# Second, a list of short names uses for the file names.
# For each parameter varied a string '_<short_name>_<value>' is appended to the log
# file names (appended to chosen prefix). Note, short names should only be letters
# from a-z or A-Z. Do not use underscores or hyphens!
# Third, the list of parameters values. If there is more than one variable this must
# be a list of tuples, each tuple having the same number of items as teh number of
# variables. Fourth, an optional dictionary with additional variables, where the keys
# are the variable names and the values are the variable values.

TPCONF_parameter_list = {
#   Vary name		V_ variable	  file name	values			extra vars
    'delays' 	    :  (['V_delay'], 	  ['del'], 	    TPCONF_delays, 		     {}),
    'loss'  	    :  (['V_loss'], 	  ['loss'], 	TPCONF_loss_rates, 	     {}),
    'tcpalgos' 	    :  (['V_tcp_cc_algo'],['tcp'], 	    TPCONF_TCP_algos, 	     {}),
    'aqms'	    :  (['V_aqm'], 	  ['aqm'], 	    TPCONF_aqms, 		     {}),
    'bsizes'	    :  (['V_bsize'], 	  ['bs'], 	    TPCONF_buffer_sizes, 	 {}),
    'runs'	    :  (['V_runs'],       ['run'], 	    range(TPCONF_runs), 	 {}),
    'bandwidths'    :  (['V_down_rate', 'V_up_rate'], ['down', 'up'], TPCONF_bandwidths, {}),
#   'transports'    :  (['V_transports'], ['transports'], TPCONF_transports,  {}),
#   'data_sizes'    :  (['V_data_size'], ['dsize'], TPCONF_data_sizes, {}),
#   'flows'         :  (['V_flows'], ['flows'], TPCONF_flows, {}),
#   'data_sizes'    :  (['V_data_size'], ['dsize'], TPCONF_data_sizes, {}),
}

# Default setting for variables (used for variables if not varied)

# The key of each item is the parameter  name. The value of each item is the default
# parameter value used if the variable is not varied.

TPCONF_variable_defaults = {
#   V_ variable			value
    'V_duration'  	:	TPCONF_duration,
    'V_delay'  		:	TPCONF_delays[0],
    'V_loss'   		:	TPCONF_loss_rates[0],
    'V_tcp_cc_algo' 	:	TPCONF_TCP_algos[0],
    'V_down_rate'   	:	TPCONF_bandwidths[0][0],
    'V_up_rate'	    	:	TPCONF_bandwidths[0][1],
#    'V_data_size'      :      TPCONF_data_sizes[0],
    'V_aqm'	    	:	TPCONF_aqms[0],
    'V_bsize'	    	:	TPCONF_buffer_sizes[0],
#    'V_data_size'       :       TPCONF_data_sizes[0],
#    'V_flows'           :       TPCONF_flows[0],
#    'V_transports'      :       TPCONF_transports[0],
}

# Specify the parameters we vary through all values, all others will be fixed
# according to TPCONF_variable_defaults
TPCONF_vary_parameters = ['delays', 'bandwidths', 'aqms','tcpalgos', 'bsizes','runs']
