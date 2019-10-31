#!/usr/bin/python3
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
  #print("\n", trafficRaw, "\n")  #TODO:DBG
  idxZero = trafficRaw.index(interface + ":")
  traffic = dict([  #TODO: shrink names
      ('ts', time.time()),                # Timestamp
      ('rx_b', trafficRaw[idxZero + 1]),  # Receive Bytes
      ('rx_p', trafficRaw[idxZero + 2]),  # Receive Packets
      ('tx_b', trafficRaw[idxZero + 9]),  # Transmit Bytes
      ('tx_p', trafficRaw[idxZero + 10])  # Transmit Packets
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
  trafficLst = list()
  with Path(filepath) as fp:
    for line in fp.read_text():
      traffic = json.dumps(line)
      if (startTS is None or traffic['ts'] >= startTS)
          and (endTS is None or traffic['ts'] <= endTS):
        history.append(traffic)
  return trafficLst


def generate_history(trafficLst):
  '''
  @func: Creates iterable of history objects.
  '''
  pass


def output_history():
  '''
  @func: Wrapper function for various output options.
  '''
  pass


def display_graph():
  '''
  @func: CLI display history as a graph.
  '''
  pass


def display_table():
  '''
  @func: CLI display history as a table.
  '''
  pass


def display_raw():
  '''
  @func: CLI display history as raw data.
  '''
  pass


def save_history():
  '''
  @func: Output history to a json file.
  '''
  pass
