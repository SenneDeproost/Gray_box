import os, sys, time
from utils import log
import utils

ARGS = sys.argv[1:]
if len(ARGS) == 0:
    COMMAND = None
else:
    COMMAND = ARGS[0]
if len(ARGS) > 1:
    PARAMS = ARGS[1:]
else:
    PARAMS = []


### --- PREPARATON --- ###
if not os.path.exists('models'):
    os.makedirs('models')

n_profiles = len([i for i in os.scandir("./models/") if os.path.isdir(i)])


### --- COMMAND PARSING --- ###

# - NO COMMAND - #
if not(COMMAND):
    COMMAND = 'info'

# - INFO - #
elif COMMAND == 'info':
    with open('.info') as f:
        print(f.read())

# - TEST - #
if COMMAND == 'test':
    print('Test received! You typed in the CLI:')
    print(PARAMS)

# - CREATE - #
if COMMAND == 'create':
    if len(PARAMS) == 0:
        profile_id = str(n_profiles + 1)
    else:
        profile_id = PARAMS[0]
    print('Creating profile with ID: ' + profile_id)
    path = 'models/' + profile_id
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        raise FileExistsError('Chosen profile ID is already made.')
    log_file = open(path + '/log', '+w')
    info_file = open(path + '/info', '+w')
    log_file.close()
    info_file.close()
    utils.LOGFILE = path + '/log'
    log('Profile created')


