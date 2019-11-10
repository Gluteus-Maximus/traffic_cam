#!/usr/bin/python3
import sys
from argparse import ArgumentParser
from pathlib import Path
import json
import time
from default_subparser import set_default_subparser


def main():
  args = getArgs()
  switch = {
      'config':   do_config,  # 
      'history':  do_history,  # 
      'auto_log': do_auto_log,  # 
      }
  return switch[args.mode](args)


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
  config.add_argument('-i', '--if', '--interface', nargs=1, type=str,
      help="###Not yet implemented")  # Interface to log
  #TODO: validate interface exists
  config.add_argument('-f', '--freq', '--frequency', nargs=1, type=int,
      help="###Not yet implemented")  # Frequency of logging
  #TODO: validate freq                                      #TODO: type??
  config.add_argument('-p', '--path', '--filepath', nargs=1, type=str,
      help="###Not yet implemented")  # Path to netdev logfile

  #TODO: need default config settings
  # APPLY SETTINGS & (RE)START CHRON JOB
  config.add_argument('-a', '--apply', action='store_true',
      help="###Not yet implemented")  # Apply config (with changes) to chronjob
  #help: changes are only applied when --apply/-a is used to restart chron job

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
  history.add_argument('-t', '--timeslice', nargs=2, metavar=('START', 'END'),
      help="###Not yet implemented ###0 for no limit, expected format is X-Y-Z")
  #TODO: validate timestamp format/0 && START<=END
  #https://stackoverflow.com/questions/21437258/how-do-i-parse-a-date-as-an-argument-with-argparse/21437360#21437360
  #history.add_argument('-p', '--path', '--filepath', nargs=1, type=str, help="")  # Path to netdev logfile

  # History Display Options
  display = history.add_mutually_exclusive_group(required=True)  #TODO: default display mode?
  display.add_argument('-g', '--graph', dest='displayMode',
      action='store_const', const='graph',
      help="###Not yet implemented")  # Graph Format
  display.add_argument('-l', '--list', dest='displayMode',
      action='store_const', const='list',
      help="###Not yet implemented")  # List Format
  history.add_argument('--hr', '--human', action='store_true',
      help="###Not yet implemented")  # Human Readable Units
  #TODO: human readable only if -g/-l (action=<check args...store_true> ?)
  #https://stackoverflow.com/questions/19414060/argparse-required-argument-y-if-x-is-present
  display.add_argument('-r', '--raw', dest='displayMode',
      action='store_const', const='raw',
      help="###Not yet implemented")  # Raw Data Format
  display.add_argument('-s', '--save', nargs=1, metavar=('SAVEFILE'),
      help="###Not yet implemented")
      #dest='displayMode', action='store_const', const='save', )  # Save Raw Data
  #TODO: change to history arg, require display unless -s used, allow -s with display arg

  ### AUTO LOG MODE ###
  # All args are required
  auto_log.add_argument('--interface', type=str, required=True)  # Interface to log
  auto_log.add_argument('--filepath', type=str, required=True)  # Path to netdev logfile

  # Set default mode to 'History'
  parser.set_default_subparser('history', insert_position=1)

  print(parser.parse_args())  #TODO:DBG
  return parser.parse_args()


def do_config(args):
  pass


def do_history(args):
  pass


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
  traffic = dict([  #TODO: shrink names  #TODO: capture interface
      ('ts', time.time()),                # Timestamp
      ('rx_b', int(trafficRaw[idxZero + 1])),  # Receive Bytes
      ('rx_p', int(trafficRaw[idxZero + 2])),  # Receive Packets
      ('tx_b', int(trafficRaw[idxZero + 9])),  # Transmit Bytes
      ('tx_p', int(trafficRaw[idxZero + 10]))  # Transmit Packets
      ])
  return traffic


def store_netdev(traffic, filepath):
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


def create_config():
  '''
  @func: Creates a config file for use by chron and splunk.
  '''
  pass


def create_chronjob():
  '''
  @func: Creates a chron job to automatically collect data.
  '''
  #TODO: allow separate files per day/hours etc
  pass


def generate_splunk_panel():
  '''
  @func: Generates a splunk panel to display histogram.
  '''
  pass


def load_netdev(filepath, startTS=None, endTS=None):
  '''
  @func: Creates iterable of netdev values.
  '''
  #TODO: handle multiple files
  trafficLst = list()
  with Path(filepath) as fp:
    for line in [x for x in fp.read_text().split("\n") if x]:
      traffic = json.loads(line)
      #TODO: json.decoder.JSONDecodeError
      if (startTS is None or traffic['ts'] >= startTS) \
          and (endTS is None or traffic['ts'] <= endTS):
        trafficLst.append(traffic)
        #TODO: skip bad entries (key/value checks)
  return trafficLst


def generate_history(trafficLst):
  '''
  @func: Creates iterable of history objects containing the difference in
    bytes and packets from the previous datum.
  '''
  if len(trafficLst) < 2:
    print("ERROR: Not enough data to generate history", file=sys.stderr)
    return None

  # Sort trafficLst by timestamp
  trafficLst = sorted([t for t in trafficLst if 'ts' in t.keys()], key = lambda x: x['ts'])
  #TODO: remove list comprehension ^ -- try/except return None
  historyLst = list()
  prevObj = trafficLst[0]
  for traffic in trafficLst[1:]:
    nextObj = traffic
    try:
      historyObj = dict([
        ('startTS', prevObj['ts']),  # Start Timestamp
        ('endTS', nextObj['ts']),  # End Timestamp
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


def output_history(historyLst, mode):
  '''
  @func: Wrapper function for various output options.
  '''
  pass


def display_graph(historyLst):
  '''
  @func: CLI display history as a graph.
  '''
  pass


def display_table(historyLst):
  '''
  @func: CLI display history as a table.
  '''
  pass


def display_raw(historyLst):
  '''
  @func: CLI display history as raw data.
  '''
  pass


def save_history(historyLst):
  '''
  @func: Output history to a json file.
  '''
  pass


if __name__ == '__main__':
  main()
