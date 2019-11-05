#!/usr/bin/python3
import sys
from argparse import ArgumentParser
from pathlib import Path
import json
import time


def getArgs(argv=sys.argv):
  parser = ArgumentParser(
      description= "Log network traffic totals and display historical trends."
      )
  parser.add_argument()
  mode = parser.add_mutually_exclusive_group()
  mode.add_argument()  # Config Mode
  mode.add_argument()  # History Mode (default)

  # CONFIG MODE
  #TODO: use nargs instead??
  #.add_argument("-i", "--interface", "--int", )  # Interface to log
  #.add_argument("-f", "--frequency", "--freq", )  # Frequency of logging
  #.add_argument("-p", "--filepath", "--path", )  # Path to netdev logfile

  # INITIATE CHRON

  # HISTORY MODE
  #.add_argument("--load", )  # Load History from File
  #.add_argument("-t", "--timeslice", nargs=2, metavar=("START", "END"))
      #TODO:check START<=END
  display = parser.add_mutually_exclusive_group()
  #.add_argument("-g", "--graph", )  # Graph Format
  #.add_argument("-l", "--list", )  # List Format
  #.add_argument("-h", "--human", )  # Human Readable Units  #TODO:-h??
  #.add_argument("-r", "--raw", )  # Raw Data Format
  #.add_argument("-s", "--save", )  # Save Raw Data


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
