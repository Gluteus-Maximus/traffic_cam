#!/usr/bin/python3
from pathlib import Path

def parse_netdev(interface):
  '''
  @return: Dictionary of network traffic values.  Values are cumulative for the
    life of the operating system.  All values are int's.
    keys: rx_bytes, rx_pkts, tx_bytes, tx_pkts
  @param interface: The network interface for which network traffic info will
    be gathered.
  '''
  netdev = Path('/proc/net/dev')
  trafficRaw = netdev.read_text().split()
  print("\n", trafficRaw, "\n")  #TODO:DBG
  idxZero = trafficRaw.index(interface + ":")
  traffic = dict([
      ('rx_bytes', trafficRaw[idxZero + 1]),
      ('rx_pkts', trafficRaw[idxZero + 2]),
      ('tx_bytes', trafficRaw[idxZero + 9]),
      ('tx_pkts', trafficRaw[idxZero + 10])
      ])
  return traffic
