#!/usr/bin/python3
'''
Adapted from ruamel/std.argparse
https://bitbucket.org/ruamel/std.argparse/
'''
import sys
import argparse


def set_default_subparser(self, name, args=None, positional_args=0, insert_position=None):
  # Use: parser.set_default_subparser( <insert arg>, insert_position=X #opt )
  """default subparser selection. Call after setup, just before parse_args()
  name: is the name of the subparser to call by default
  args: if set is the argument list handed to parse_args()

  , tested with 2.7, 3.2, 3.3, 3.4
  it works with 2.6 assuming argparse is installed
  """
  subparser_found = False
  for arg in sys.argv[1:]:
    if arg in ['-h', '--help']:  # global help if no subparser
      break
  else:
    for x in self._subparsers._actions:
      if not isinstance(x, argparse._SubParsersAction):
        continue
      for sp_name in x._name_parser_map.keys():
        if sp_name in sys.argv[1:]:
          subparser_found = True
    if not subparser_found:
      # insert default in last position before global positional
      # arguments, this implies no global options are specified after
      # first positional argument
      if args is None:
        if insert_position is None:
          sys.argv.insert(len(sys.argv) - positional_args, name)
        else:
          sys.argv.insert(insert_position, name) # Insert at specified position
      else:
        if insert_position is None:
          args.insert(len(args) - positional_args, name)
        else:
          args.insert(insert_position, name) # Insert at specified position

argparse.ArgumentParser.set_default_subparser = set_default_subparser
