#!/usr/bin/python3
import sys
#from argparse import
from pathlib import Path
import json
import time

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
  idxZero = trafficRaw.index(interface + ":")
  traffic = dict([  #TODO: shrink names
      ('ts', time.time()),                     # Timestamp
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


def output_history(mode, historyLst, filepath=None):
  '''
  @func: Wrapper function for various output options.
  '''
  #TODO: validation?
  # Filepath validation for 'save' mode happens during arg parsing
  #filepath = read_config()['default_save_filepath'] if not filepath  #TODO ??
  switch = {
      'graph': display_graph,
      'table': display_table,
      'raw'  : display_raw,
      'save' : save_history
      }
  # Call function from 'switch' according to 'mode'
  return switch[mode](historyLst, filepath)
    # 'filepath' is ignored where appropriate
  pass


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
