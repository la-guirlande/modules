"""Project entry point.

To run any feature from this project, this file is the entry point and must be executed as a script.

Available features :
- `main.py start <MODULE_TYPE>` : Starts a module
- `main.py package` : Packages all modules

For more details, run `main.py -h`.

"""
import argparse
from modules.utils import project

parser = argparse.ArgumentParser(description='Module starter script')

subparsers = parser.add_subparsers(help='Sub commands', dest='sub_command')

parser_start = subparsers.add_parser('start', help='Starts a module')
parser_start.add_argument('module', type=str, choices=list(map(lambda t: t.name.lower(), project.ModuleType)), help='Module to start')

parser_package = subparsers.add_parser('package', help='Packaging modules')
parser_package.add_argument('-a', '--all', help='Packages all modules')

args = parser.parse_args()

match args.sub_command:
  case 'start':
    from scripts import start
    start.start(args.module)
  case 'package':
    from scripts import package
    package.start()
  case _:
    print('Unknown subcommand')
