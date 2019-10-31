#!/usr/bin/python3
from pathlib import Path
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
  traffic = dict([
      ('timestamp', time.time()),
      ('rx_bytes', trafficRaw[idxZero + 1]),
      ('rx_pkts', trafficRaw[idxZero + 2]),
      ('tx_bytes', trafficRaw[idxZero + 9]),
      ('tx_pkts', trafficRaw[idxZero + 10])
      ])
  return traffic


def store_netdev(traffic, filepath):
  '''
  @func: Saves a snapshot of /proc/net/dev to the json file at filepath.
  @return: 0 for success, 1 for failure
  '''
  pass


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


def generate_history():
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
