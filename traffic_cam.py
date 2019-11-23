#!/usr/bin/python3
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
import json
import time
from default_subparser import set_default_subparser
#TODO: human readable module


#TODO: this file must be owned by root/su, executable by all if possible
#TODO: filewide: raise <exc>() from e


### CONFIG DEFAULT VALUES ###
configFile = '.traffic_cam.conf'
configDefaults = {
    'interface': 'eth0',
    'frequency': 1,
    'filepath':  'netdev.log'
    }
errorFilepath = '/var/log/traffic_cam.log'
cronFilepath = '/etc/cron.d/traffic_cam_cron'


def main():
  '''
  @func: Primary handler function for program.
  '''
  args = get_args()
  switch = {
      'config':   do_config,    # 
      'history':  do_history,   # 
      'auto_log': do_auto_log,  # 
      }
  try:
    return switch[args.mode](args)
  except Exception as e:
    print(e, file=sys.stderr)
    return 1


def get_args(argv=sys.argv):
  '''
  @func: Parses arguments for program and provides help (-h) dialogue. Provides
    three modes: config, history, and auto_log.
    > Config mode should be run as root, and allows the user to set config
    options and start or stop the auto logger cronjob.
    > Auto_log mode is called by the cronjob to automatically parse and store
    network traffic data. This mode is hidden from the user.
    > History mode allows the user to examine the historical trends of network
    traffic in several formats.
  '''
  parser = ArgumentParser(
      description="Log network traffic totals and display historical trends."
      )
  ### 'MODE' SUBPARSERS ###
  #TODO: how to add 'action' to subparser call (ie. set mode string)
  mode = parser.add_subparsers(dest='mode', metavar='MODE',
      help="###SUBPARSER HELP### default history", )  #TODO
  config = mode.add_parser('config', #action='store_true',
      help="###Program Configuration Help###")  # Config Mode #TODO
  history = mode.add_parser('history',
      help="###History Display Help###")  # History Mode (default) #TODO
  # auto_log mode hidden from help dialogue, user shouldn't interact with this
  auto_log = mode.add_parser('auto_log',
      add_help=False) #help="###Auto-Logger Help###")  # Auto Log Mode #TODO

  ### CONFIG MODE ARGS ###
  #TODO: add status??
  #TODO: add auto history
  #TODO: help *4
  #TODO: input validation -- https://stackoverflow.com/questions/14117415/in-python-using-argparse-allow-only-positive-integers
  config.add_argument('-i', '--interface', dest='interface', type=str,
      help="###Not yet implemented")  # Interface to log
  #TODO: validate interface exists
  #TODO: !!! ELIMINATE FREQUENCY. ONCE PER 30S !!!
  config.add_argument('-f', '--frequency', dest='frequency', type=int,
      help="###Not yet implemented - recommend even divisible into hour")  # Frequency of logging
                                                            #TODO: type??
  config.add_argument('-p', '--filepath', dest='filepath', type=str,
      help="###Not yet implemented")  # Path to netdev logfile

  #TODO: need default config settings
  # START/STOP CRON JOB
  cron = config.add_mutually_exclusive_group()
  cron.add_argument('-a', '--apply', action='store_true',
      help="###Not yet implemented -- need sudo/root")  # Apply config (with changes) to cronjob
  #help: changes are only applied when --apply/-a is used to restart cron job
  cron.add_argument('-k', '--kill', action='store_true',
      help="###Not yet implemented -- need sudo/root??")  # Delete cron job (if exists)

  # CREATE SPLUNK PANEL
  #config.add_argument('-s', '--splunk', action='store_true', help="")  # Create Splunk Panel with Current Config
  #TODO

  ### HISTORY MODE ARGS ###
  source = history.add_mutually_exclusive_group(required=False)
  source.add_argument('--load', nargs=1, type=str, metavar=('HISTORYFILE'),
      help="###Not yet implemented")  # Load Saved History from File
  #TODO: validate filepath
  source.add_argument('--logfiles', nargs='+', type=str,
      help="###Not yet implemented")  # Specify Input NetDev Logfile(s) (if different from filepath in config)
  history.add_argument('--timeslice', '--time', nargs=2, type=float, metavar=('START', 'END'),
      help="###Not yet implemented ###0 for no limit, expected format is X-Y-Z, -Y/-Z for Y/Z minutes ago.")
  #TODO: validate timestamp format/0 && START<=END
  #https://stackoverflow.com/questions/21437258/how-do-i-parse-a-date-as-an-argument-with-argparse/21437360#21437360
  #history.add_argument('-p', '--path', '--filepath', nargs=1, type=str, help="")  # Path to netdev logfile
  #TODO: timestamp format string?

  # History Display Options
  display = history.add_mutually_exclusive_group(required=True)  #TODO: default display mode?
  display.add_argument('-g', '--graph', dest='outputMode',
      action='store_const', const='graph',
      help="###Not yet implemented")  # Graph Format
  display.add_argument('-l', '--list', dest='outputMode',
      action='store_const', const='list',
      help="###Not yet implemented")  # List Format #TODO: remove??
  display.add_argument('-t', '--table', dest='outputMode',
      action='store_const', const='table',
      help="###Not yet implemented")  # List Format
  display.add_argument('-r', '--raw', dest='outputMode',
      action='store_const', const='raw',
      help="###Not yet implemented")  # Raw Data Format
  display.add_argument('-a', '--average', dest='outputMode',  #TODO: make this default
      action='store_const', const='average',
      help="###Not yet implemented")  # Raw Data Format
  display.add_argument('-s', '--save', nargs=1, metavar=('SAVEFILE'),
      help="###Not yet implemented")
      #dest='outputMode', action='store_const', const='save', )  # Save Raw Data
  #TODO: change to history arg, require display unless -s used, allow -s with display arg
  history.add_argument('--hr', '--human', dest='human', action='store_true',
      help="###Not yet implemented")  # Human Readable Units
  #TODO: human readable only if -g/-l (action=<check args...store_true> ?)
  #https://stackoverflow.com/questions/19414060/argparse-required-argument-y-if-x-is-present

  ### AUTO LOG MODE ARGS ###
  #TODO: add splunk panel mode
  # All args are required
  auto_log.add_argument('-i', '--interface', type=str, required=True)  # Interface to log
  auto_log.add_argument('-p', '--filepath', type=str, required=True)  # Path to netdev logfile

  # Set default mode to 'History'
  parser.set_default_subparser('history', insert_position=1)

  print("DEBUG:", parser.parse_args())  #TODO:DBG
  return parser.parse_args()


def load_config(filepath=configFile):
  '''
  @func: Loads and returns config settings.
  @param: filepath: Relative path to program config file.
  @return: Dictionary of settings.
  '''
  try:
    #TODO: fix relative path
    fp = Path(filepath)
    return json.loads(fp.read_text())
  except FileNotFoundError as e:
    raise Exception(
        "CONFIG ERROR: config file missing - './traffic_cam config -h'"
        ) from e
  except json.decoder.JSONDecodeError as e:
    raise Exception(
        "CONFIG ERROR: bad config file - './traffic_cam config -h'",
        ) from e  #TODO: raise error, exit
  #TODO: how to differentiate between raised exceptions?


### CONFIG MODE ###
#TODO: !!! ELIMINATE FREQUENCY. ONCE PER 30S !!!
#TODO: STORYBOARD THIS FUNCTION!!!
#TODO: MUST BE ROOT/SU FOR MODE
#TODO: ALL FILES SHOULD BE OWNED BY ROOT (except logs)
#TODO: store target owner of log files in config?
def do_config(args):
  '''
  @func: Config Mode - modify and apply configuration changes, manage automatic
    data logging cronjob.
  @param: args: Namespace of argument parser.
  '''
  configs = None
  try:
    configs = load_config()
  except Exception as e:
    print(e, file=sys.stderr)  # warn user and continue
    #TODO: print warning
    #TODO: create new .conf? warn and user creates? create here (attempt), warn/quit elsewhere
  # Add any missing keys to existing config (attempts to correct)
  if configs is None:
    configs = configDefaults
  else:
    for key, value in configDefaults.items():
      if key not in configs.keys():  #TODO: correct or error out???
        configs[key] = value
  configs['interface'] = args.interface if args.interface else configs['interface']
  configs['frequency'] = args.frequency if args.frequency else configs['frequency']
  configs['filepath'] = args.filepath if args.filepath else configs['filepath']  #TODO: rename - netdev
  try:
    validate_configs(configs)
  except Exception as e:
    raise Exception(e)
  with Path(configFile) as fp:  #TODO: os.path.dirname(os.path.realpath(__file__))
    try:
      fp.write_text(json.dumps(configs)) #TODO: no need to attempt if no changes needed
    except Exception as e:  #TODO: write access exception (x2)
      raise Exception(e)
  print(configs)  #TODO DBG
  try:
    if args.apply is True:
      delete_cronjob()
      create_cronjob(configs)
    elif args.kill is True:
      delete_cronjob()
  except Exception as e:  #TODO: specify exception (x2)
    raise Exception(e)
  return 0


def validate_configs(configs):
  #TODO: function string
  errors = list()
  try:
    validate_interfaces(configs['interface'])
  except Exception as e:
    errors.append(e)
  try:
    validate_frequency(configs['frequency'])
  except Exception as e:
    errors.append(e)
  try:
    validate_filepath(configs['filepath'])  #TODO: rename - netdev
  except Exception as e:
    errors.append(e)
  if errors:
    raise Exception(("CONFIG ERROR: './traffic_cam config -h' for help" + \
        "\n{}"*len(errors)).format(*errors))


def validate_interfaces(interface):
  #TODO: function string
  if interface not in get_interfaces():
    #TODO: specify exception
    raise Exception("Interface does not exist: '{}'".format(interface))


def get_interfaces():
  #TODO: function string
  netdev = Path('/proc/net/dev')
  netdevRaw = netdev.read_text().split()
  #TODO: validate fields exist
  interfaces = list()
  idx = 20  # First interface idx (skip header strings)
  while idx < len(netdevRaw):
    interfaces.append(netdevRaw[idx].strip(":"))
    idx += 17
  return interfaces


#TODO: !!! ELIMINATE FREQUENCY. ONCE PER 30S !!!
def validate_frequency(frequency):
  #TODO: function string
  if type(frequency) is not int or frequency < 1 or frequency > 60:
    raise Exception("Frequency must be a number between 1 and 60")


def validate_filepath(filepath):
  #TODO: function string
  try:
    with open(filepath, 'a'):  #TODO: chmod +rw
      pass
  except OSError as e:
    raise OSError(e)  #TODO: remove '[Errno \d+]' - regex


def create_cronjob(configs):
  #TODO: dynamic program name (sys.argv[0])
  #TODO: add to PATH if not there (no abs/rel pathing)
  #TODO: expand filepath to absolute
  #TODO: build separate module and API for this for future use
  '''
  @func: Creates a cron job to automatically collect data.
  '''
  if not is_super_user():  #TODO: try/exc on file creation instead
    raise Exception("ERROR: Must be root.")
  programPath = os.path.realpath(__file__)
  #TODO: add error output 2>> {dir(programPath)/error.log}
  # 0=dir 1=freq 2=interface 3=output filepath
  netdevCronStr = \
      "*/{1} * * * * root {0} auto_log -i {2} -p {3}".format(
          programPath,
          configs['frequency'],
          configs['interface'],
          os.path.realpath(configs['filepath']) )  #TODO: rename - netdev
  # 0=dir 1=freq 2=output filepath
  historyCronStr = \
      "*/{1} * * * * root {0} history -s {2} --time {3} {4}".format(
          programPath,
          configs['frequency'],
          0, #os.path.realpath(configs['save']),  #TODO
          0, #configs['startTS'],
          0  #configs['endTS']
          )
  # 0=dir 1=netdev_cron 2=history_cron
  historyCronStr = ""  #TODO DBG
  cronStr = ''' \
# /etc/cron.d/traffic_cam_cron: cron.d entries for the traffic_cam package
SHELL=/bin/sh

{0}
{1}
  '''.format(netdevCronStr, historyCronStr)
  try:
    with Path(cronFilepath).open('w+') as fp:  #TODO: change mode to create
      fp.write(cronStr)
  except Exception as e:  #TODO: specify
    raise Exception("ERROR: {}".format(e))


def delete_cronjob():
  #TODO: function string
  #TODO: dynamic program name (sys.argv[0])
  if not is_super_user():  #TODO: try/exc on file creation instead
    raise Exception("ERROR: Must be root.")
  try:
    os.remove(cronFilepath)
  except Exception as e:  #TODO: specify
    raise Exception("ERROR: {}".format(e))


def is_super_user():
  #TODO
  return True


def generate_splunk_panel():
  '''
  @func: Generates a splunk panel to display histogram.
  '''
  pass


### HISTORY MODE ###
#TODO: static headers (move with scroll)
#TODO: add auto history function for auto_log to use in splunk panel mode
def do_history(args):
  #TODO: function string
  '''
  '''
  # populate null timeslice
  if args.timeslice is None:
    args.timeslice = (0, 0)

  # offset timeslice for negative values
  for idx, val in enumerate(args.timeslice):
    if val < 0:
      args.timeslice[idx] = time.time() - (-val * 60)

  # create historyLst
  if args.load:
    historyLst = load_history(args.load,
        args.timeslice[0], args.timeslice[1], args.human)
  else:
    if args.logfiles:
      trafficLst = load_netdev(args.logfiles,
          args.timeslice[0], args.timeslice[1])
    else:
      config = load_config()
      trafficLst = load_netdev([config['filepath']],
          args.timeslice[0], args.timeslice[1])
    historyLst = generate_history(trafficLst, args.human)

  if historyLst is None:
    return 0

  return output_history(args.outputMode, historyLst, args.save, args.human)


def load_netdev(files, startTS=0, endTS=0):
  #TODO: cleanup!
  #TODO: handle negative timeslice
  '''
  @func: Creates iterable of netdev values.
  @return: List of traffic dict's
  '''
  trafficLst = list()
  for filepath in files:
    try:
      with Path(filepath) as fp:
        for line in [x for x in fp.read_text().split("\n") if x]:
          try:
            traffic = json.loads(line)
            if (startTS == 0 or traffic['ts'] >= startTS) \
                and (endTS == 0 or traffic['ts'] <= endTS):
              #TODO: validate all fields
              trafficLst.append(traffic)
          except (KeyError, json.decoder.JSONDecodeError) as e:
            # skip bad entries
            #print("ERROR: skipping bad line {}".format(e), file=sys.stderr)
            continue
    except Exception as e:  #TODO: target exceptions
      print("ERROR: {}".format(e), file=sys.stderr)
  return trafficLst if trafficLst else None


def generate_history(trafficLst, humanRead=False):
  #TODO: DROP NEGATIVE VALUE EVENTS!
  '''
  @func: Creates iterable of history objects containing the difference in
    bytes and packets from the previous datum.
  '''
  #TODO: omit None?
  if trafficLst is None or len(trafficLst) < 2:
    print("ERROR: Not enough data to generate history", file=sys.stderr)
    #TODO: raise error
    return None

  # Sort trafficLst by timestamp, drop bad entries
  netdevKeys = set(['if', 'ts', 'rx_b', 'rx_p', 'tx_b', 'tx_p'])  #TODO: link to parse_netdev
  trafficLst = sorted(
      [t for t in trafficLst if set(t.keys()) == netdevKeys],
      key = lambda x: x['ts']
      )
  #TODO: remove list comprehension ^ -- try/except skip
  historyLst = list()
  prevObj = trafficLst[0]
  for traffic in trafficLst[1:]:
    nextObj = traffic
    try:
      historyObj = dict([
        ('startTS', prevObj['ts']),  # Start Timestamp
        ('endTS', nextObj['ts']),    # End Timestamp
        ('rx_b', nextObj['rx_b']),   # Receive Bytes
        ('rx_p', nextObj['rx_p']),   # Receive Packets
        ('tx_b', nextObj['tx_b']),   # Transmit Bytes
        ('tx_p', nextObj['tx_p']),   # Transmit Packets
        ])
      if (historyObj['rx_b'] - prevObj['rx_b']) >= 0:  # Skips rollover events
        historyObj['rx_b'] -= prevObj['rx_b']  # Diff Receive Bytes
        historyObj['rx_p'] -= prevObj['rx_p']  # Diff Receive Packets
        historyObj['tx_b'] -= prevObj['tx_b']  # Diff Transmit Bytes
        historyObj['tx_p'] -= prevObj['tx_p']  # Diff Transmit Packets
      historyLst.append(historyObj)
    except KeyError:
      print("ERROR: Skipping bad entry in dataset", file=sys.stderr)
      continue
    prevObj = traffic
  return historyLst


def load_history(filepath, startTS=0, endTS=0):
  '''
  @func: Creates a history list from json history file.
  @return: List of history dict's (equiv. to historyLst)
  '''
  #TODO: handle multiple files
  #TODO: overload load_netdev??
  try:
    with Path(filepath) as fp:
      historyLst = list()
      for line in [x for x in fp.read_text().split("\n") if x]:
        traffic = json.loads(line)
        #TODO: json.decoder.JSONDecodeError
        if (startTS == 0 or traffic['startTS'] >= startTS) \
            and (endTS == 0 or traffic['endTS'] <= endTS):
          historyLst.append(traffic)
        #TODO: skip bad entries (key/value checks) - try/except
      return historyLst
  except Exception as e:  #TODO: target exceptions
    print("ERROR: {}".format(e), file=sys.stderr)
    return None


def output_history(outputMode, historyLst, filepath=None, humanRead=False):
  '''
  @func: Wrapper function for various output options.
  '''
  #TODO: validation?
  # Filepath validation for 'save' mode happens during arg parsing
  #filepath = read_config()['default_save_filepath'] if not filepath  #TODO ??
  switch = {
      'graph'  : display_graph,
      'table'  : display_table,
      'list'   : display_list,
      'raw'    : display_raw,
      'save'   : save_history,
      'average': display_average
      }
  # Call function from 'switch' according to 'mode'
  return switch[outputMode](historyLst, filepath, humanRead)
    # 'filepath' is ignored where appropriate


def display_graph(historyLst, _, humanRead):
  '''
  @func: CLI display history as a graph.
  '''
  print("display_graph")  #TODO DBG
  return 0
  pass


def display_table(historyLst, _, humanRead):
  '''
  @func: CLI display history as a table.
  '''
  if not historyLst:
    return 1
  print("Timestamp.....RX Bytes.....RX Packets.....TX Bytes.....TX Packets")
  for item in historyLst:
    #TODO: fix format, use ascii lines
    print("{} | {} | {} | {} | {}".format(
      time.ctime(item['endTS']), item['rx_b'], item['rx_p'], item['tx_b'], item['tx_p'])
      )
  return 0


def display_list(historyLst, _, humanRead):
  '''
  @func: CLI display history as a list.
  '''
  print("display_list")  #TODO DBG
  return 0


def display_raw(historyLst, *_):
  '''
  @func: CLI display history as raw data.
  '''
  for item in historyLst:
    print(item)
  return 0


def save_history(historyLst, filepath, _):
  '''
  @func: Output history to a json file. Overwrites file if exists.
    Always stores raw values (byte count and epoch timestamps).
  '''
  #TODO: specify target file owner?
  #TODO: try/exc file
  for item in historyLst:
    store_netdev(item, filepath)
  return 0


def display_average(historyLst, _, humanRead):
  '''
  '''
  #TODO: try/exc
  # Print time range
  minTS = min(historyLst, key=lambda x: x['startTS'])['startTS']
  maxTS = max(historyLst, key=lambda x: x['endTS'])['endTS']
  print("Average Utilization: '{}' to '{}'\n".format(
      time.ctime(minTS),
      time.ctime(maxTS)))
  # Calc and print averages
  rx_b = [x['rx_b'] for x in historyLst]
  rx_b = sum(rx_b) / (maxTS - minTS)
  rx_p = [x['rx_p'] for x in historyLst]
  rx_p = sum(rx_p) / (maxTS - minTS)
  tx_b = [x['tx_b'] for x in historyLst]
  tx_b = sum(tx_b) / (maxTS - minTS)
  tx_p = [x['tx_p'] for x in historyLst]
  tx_p = sum(tx_p) / (maxTS - minTS)
  averageStr = '''\
Receive Data
 {0:0.0f} {1}/s
Receive Packets
 {2:0.2f} pkt/s
Transmit Data
 {3:0.0f} {4}/s
Transmit Packets
 {5:0.2f} pkt/s'''
  print(averageStr.format(*(rx_b, "B"), rx_p, *(tx_b, "B"), tx_p))  #TODO: B/MB/GB
  return 0


### AUTO LOG MODE ###
def do_auto_log(args):
  #TODO: send errors to error log
  #TODO: try
  traffic = parse_netdev(args.interface)
  store_netdev(traffic, args.filepath)
  return 0


def parse_netdev(interface):
  '''
  @func: Extracts relevant data from /proc/net/dev and returns as a dict.
  @return: Dictionary of network traffic values.  Values are cumulative for the
    life of the operating system.  All values are int's.
    keys: rx_bytes, rx_pkts, tx_bytes, tx_pkts
  @param interface: The network interface for which network traffic info will
    be gathered.
  '''
  netdev = Path('/proc/net/dev')
  trafficRaw = netdev.read_text().split()
  #TODO: validate fields exist
  #TODO: try interface name, exception if not present
  idxZero = trafficRaw.index(interface + ":")
  traffic = dict([  #TODO: shrink names
      ('if', interface),                       # Interface
      ('ts', int(time.time())),                # Timestamp
      ('rx_b', int(trafficRaw[idxZero + 1])),  # Receive Bytes
      ('rx_p', int(trafficRaw[idxZero + 2])),  # Receive Packets
      ('tx_b', int(trafficRaw[idxZero + 9])),  # Transmit Bytes
      ('tx_p', int(trafficRaw[idxZero + 10]))  # Transmit Packets
      ])
  return traffic


def store_netdev(traffic, filepath):  #TODO: rename to store_dict
  '''
  @func: Saves a snapshot of /proc/net/dev to the json file at filepath.
  @return: 0 for success, 1 for failure
  '''
  #TODO: specify target file owner?
  try:
    with Path(filepath).open(mode='a') as fp:
      fp.write(json.dumps(traffic) + "\n")
    return 0
  except Exception as e:  #TODO: specify
    print("SAVE ERROR: {}".format(e))
    return 1


if __name__ == '__main__':
  main()
