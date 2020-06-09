import os, sys
import argparse
print('* ------------------------------------------------- *')
print('*                  Gray Box v0.01                   *')
print('*     by Senne Deproost, senne.deproost@vub.be      *')
print('* ------------------------------------------------- *')

ARGS = sys.argv[1:]
COMMAND = ARGS[0]
if len(ARGS) > 2:
    PARAMS = ARGS[1:]

### --- COMMAND PARSING --- ###

# - TEST - #
if COMMAND == "test":
    print('Test received! You typed in the CLI:')
    print(PARAMS)
