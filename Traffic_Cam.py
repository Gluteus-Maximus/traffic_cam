#!/usr/bin/python3
import sys
from argparse import ArgumentParser
from pathlib import Path
import json
import time
from default_subparser import set_default_subparser


### CONFIG DEFAULT VALUES ###
configFile = '.traffic_cam.conf'
configDefaults = {
    'interface': 'eth0',
    'frequency': 1,
    'filepath':  'netdev.log'
    }


def main():
  args = getArgs()
  switch = {
      'config':   do_config,  # 
      'history':  do_history,  # 
      'auto_log': do_auto_log,  # 
      }
  try:
    return switch[args.mode](args)
  except Exception as e:
    print(e, file=sys.stderr)
    return 1


def getArgs(argv=sys.argv):
  #TODO: function string
  '''
  '''
  parser = ArgumentParser(
      description= "Log network traffic totals and display historical trends."
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

  ### CONFIG MODE ###
  #TODO: help *4
  #TODO: input validation -- https://stackoverflow.com/questions/14117415/in-python-using-argparse-allow-only-positive-integers
  config.add_argument('-i', '--interface', dest='interface', type=str,
      help="###Not yet implemented")  # Interface to log
  #TODO: validate interface exists
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

  ### HISTORY MODE ###
  source = history.add_mutually_exclusive_group(required=False)
  source.add_argument('--load', nargs=1, type=str, metavar=('HISTORYFILE'),
      help="###Not yet implemented")  # Load Saved History from File
  #TODO: validate filepath
  source.add_argument('--logfiles', nargs='+', type=str,
      help="###Not yet implemented")  # Specify Input NetDev Logfile(s) (if different from filepath in config)
  history.add_argument('--timeslice', '--time', nargs=2, type=float, metavar=('START', 'END'),
      help="###Not yet implemented ###0 for no limit, expected format is X-Y-Z")
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
  history.add_argument('--hr', '--human', dest='human', action='store_true',
      help="###Not yet implemented")  # Human Readable Units
  #TODO: human readable only if -g/-l (action=<check args...store_true> ?)
  #https://stackoverflow.com/questions/19414060/argparse-required-argument-y-if-x-is-present
  display.add_argument('-r', '--raw', dest='outputMode',
      action='store_const', const='raw',
      help="###Not yet implemented")  # Raw Data Format
  display.add_argument('-s', '--save', nargs=1, metavar=('SAVEFILE'),
      help="###Not yet implemented")
      #dest='outputMode', action='store_const', const='save', )  # Save Raw Data
  #TODO: change to history arg, require display unless -s used, allow -s with display arg

  ### AUTO LOG MODE ###
  # All args are required
  auto_log.add_argument('--interface', type=str, required=True)  # Interface to log
  auto_log.add_argument('--filepath', type=str, required=True)  # Path to netdev logfile

  # Set default mode to 'History'
  parser.set_default_subparser('history', insert_position=1)

  print("DEBUG:", parser.parse_args())  #TODO:DBG
  return parser.parse_args()


def load_config(filepath=configFile):
  '''
  @func: Loads and returns config settings.
  @return: Dictionary of settings.
  '''
  try:
    fp = Path(filepath)
    return json.loads(fp.read_text())
  except FileNotFoundError as e:
    #print("ERROR: {}".format(e), file=sys.stderr)  #TODO: raise error, exit
    print("ERROR: config file missing - './traffic_cam config -h'".format(e), file=sys.stderr)  #TODO: raise error, exit
  except json.decoder.JSONDecodeError as e:
    print("ERROR: bad config file", file=sys.stderr)  #TODO: raise error, exit
  #TODO: how to differentiate between raised exceptions?


### CONFIG MODE ###
#TODO: STORYBOARD THIS FUNCTION!!!
def do_config(args):
  print("do_config")  #TODO DBG
  try:
    configs = load_config()
  except:
    print("ERROR: {}") #TODO: raise error in load_config
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
  configs['filepath'] = args.filepath if args.filepath else configs['filepath']
  try:
    validate_config(configs)
  except Exception as e:
    raise Exception(e)
  with Path(configFile) as fp:
    try:
      fp.write_text(json.dumps(configs)) #TODO: no need to attempt if no changes needed
    except Exception as e:  #TODO: write access exception (x2)
      raise Exception(e)
  try:
    if args.apply is True:
      delete_cronjob()
      create_cronjob(configs)
    elif args.kill is True:
      delete_cronjob()
  except Exception as e:  #TODO: specify exception (x2)
    raise Exception(e)
  return 0


#TODO: XXX
def create_config(interface=None, frequency=None, filepath=None):
  '''
  @func: Creates a config file for use by cron and splunk.
  '''
  pass


def validate_config(configs):
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
    validate_filepath(configs['filepath'])
  except Exception as e:
    errors.append(e)
  if errors:
    raise Exception(("CONFIG ERROR: './traffic_cam config -h' for help" + \
        "\n{}"*len(errors)).format(*errors))  #TODO DBG


def validate_interfaces(interface):
  if interface not in get_interfaces():
    #TODO: specify exception
    raise Exception("Interface does not exist: '{}'".format(interface))


def get_interfaces():
  netdev = Path('/proc/net/dev')
  netdevRaw = netdev.read_text().split()
  #TODO: validate fields exist
  interfaces = list()
  idx = 20  # First interface idx (skip header strings)
  while idx < len(netdevRaw):
    interfaces.append(netdevRaw[idx].strip(":"))
    idx += 17
  return interfaces


def validate_frequency(frequency):
  if type(frequency) is not int or frequency < 1 or frequency > 60:
    raise Exception("Frequency must be a number between 1 and 60")


def create_cronjob(configs):
  #TODO: dynamic program name (sys.argv[0])
  #TODO: add to PATH if not there (no abs/rel pathing)
  '''
  @func: Creates a cron job to automatically collect data.
  '''
  #TODO: build separate module and API for this for future use
    #TODO: allow separate files per day/hours etc
  pass


def delete_cronjob():
  #TODO: dynamic program name (sys.argv[0])
  pass


def generate_splunk_panel():
  '''
  @func: Generates a splunk panel to display histogram.
  '''
  pass


### HISTORY MODE ###
def do_history(args):
  '''
  '''
  # format timeslice
  if args.timeslice is None:
    args.timeslice = (None, None)
  else:
    if args.timeslice[0] == 0:
      args.timeslice[0] = None
    if args.timeslice[1] == 0:
      args.timeslice[1] = None

  # create historyLst
  if args.load:
    historyLst = load_history(args.load,
        args.timeslice[0], args.timeslice[1], args.human)
  else:
    if args.logfiles:
      trafficLst = load_netdev(args.logfiles,
          args.timeslice[0], args.timeslice[1], args.human)
    else:
      config = load_config()
      trafficLst = load_netdev([config['filepath']],
          args.timeslice[0], args.timeslice[1])
    historyLst = generate_history(trafficLst, args.human)

  if historyLst is None:
    return 0

  return output_history(args.outputMode, historyLst, args.save)


def load_netdev(files, startTS=None, endTS=None):
  #TODO: cleanup!
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
            #TODO: json.decoder.JSONDecodeError
            if (startTS is None or traffic['ts'] >= startTS) \
                and (endTS is None or traffic['ts'] <= endTS):
              trafficLst.append(traffic)
              #TODO: skip bad entries (key/value checks) - try, continue
          except KeyError as e:
            #print("ERROR: skipping bad line {}".format(e), file=sys.stderr)
            continue
    except Exception as e:  #TODO: target exceptions
      print("ERROR: {}".format(e), file=sys.stderr)
  return trafficLst if trafficLst else None


def generate_history(trafficLst, humanRead=False):
  '''
  @func: Creates iterable of history objects containing the difference in
    bytes and packets from the previous datum.
  '''
  #TODO: omit None?
  if trafficLst is None or len(trafficLst) < 2:
    print("ERROR: Not enough data to generate history", file=sys.stderr)
    #TODO: raise error
    return None

  # Sort trafficLst by timestamp
  trafficLst = sorted([t for t in trafficLst if 'ts' in t.keys()], key = lambda x: x['ts'])
  #TODO: remove list comprehension ^ -- try/except skip
  historyLst = list()
  prevObj = trafficLst[0]
  for traffic in trafficLst[1:]:
    nextObj = traffic
    try:
      historyObj = dict([
        ('startTS', prevObj['ts']),                   # Start Timestamp
        ('endTS', nextObj['ts']),                     # End Timestamp
        ('rx_b', nextObj['rx_b'] - prevObj['rx_b']),  # Diff Receive Bytes
        ('rx_p', nextObj['rx_p'] - prevObj['rx_p']),  # Diff Receive Packets
        ('tx_b', nextObj['tx_b'] - prevObj['tx_b']),  # Diff Transmit Bytes
        ('tx_p', nextObj['tx_p'] - prevObj['tx_p']),  # Diff Transmit Packets
        ])
      historyLst.append(historyObj)
    except KeyError:
      print("ERROR: Skipping bad entry in dataset", file=sys.stderr)
    prevObj = traffic
  return historyLst


def load_history(filepath, startTS=None, endTS=None, humanRead=False):
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
        if (startTS is None or traffic['startTS'] >= startTS) \
            and (endTS is None or traffic['endTS'] <= endTS):
          historyLst.append(traffic)
        #TODO: skip bad entries (key/value checks) - try/except
      return historyLst
  except Exception as e:  #TODO: target exceptions
    print("ERROR: {}".format(e), file=sys.stderr)
    return None


def output_history(outputMode, historyLst, filepath=None):
  '''
  @func: Wrapper function for various output options.
  '''
  #TODO: validation?
  # Filepath validation for 'save' mode happens during arg parsing
  #filepath = read_config()['default_save_filepath'] if not filepath  #TODO ??
  switch = {
      'graph': display_graph,
      'table': display_table,
      'list' : display_list,
      'raw'  : display_raw,
      'save' : save_history
      }
  # Call function from 'switch' according to 'mode'
  return switch[outputMode](historyLst, filepath)
    # 'filepath' is ignored where appropriate


def display_graph(historyLst, _):
  '''
  @func: CLI display history as a graph.
  '''
  print("display_graph")  #TODO DBG
  pass


def display_table(historyLst, _):
  '''
  @func: CLI display history as a table.
  '''
  print("display_table")  #TODO DBG
  if not historyLst:
    return
  print("Timestamp.....RX Bytes.....RX Packets.....TX Bytes.....TX Packets")
  for item in historyLst:
    #TODO: fix format, use ascii lines
    print("{} | {} | {} | {} | {}".format(
      item['endTS'], item['rx_b'], item['rx_p'], item['tx_b'], item['tx_p'])
      )


def display_list(historyLst, _):
  '''
  @func: CLI display history as a list.
  '''
  print("display_list")  #TODO DBG
  pass


def display_raw(historyLst, _):
  '''
  @func: CLI display history as raw data.
  '''
  for item in historyLst:
    print(item)


def save_history(historyLst, filepath):
  '''
  @func: Output history to a json file. Overwrites file if exists.
  '''
  for item in historyLst:
    store_netdev(item, filepath)


### AUTO LOG MODE ###
def do_auto_log(args):
  pass


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
  idxZero = trafficRaw.index(interface + ":")
  traffic = dict([  #TODO: shrink names
      ('if', interface),                       # Interface
      ('ts', time.time()),                     # Timestamp
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
  try:
    with Path(filepath).open(mode='a') as fp:
      fp.write(json.dumps(traffic) + "\n")
    return 0
  except Exception as e:  #TODO: specify
    print("SAVE ERROR: {}".format(e))
    return 1


if __name__ == '__main__':
  main()
