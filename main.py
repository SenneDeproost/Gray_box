import os
import shutil
import sys

import utils
from utils import log
import distillation as dis

global COMMAND

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
if not os.path.exists('profiles'):
    os.makedirs('profiles')

n_profiles = len([i for i in os.scandir("./profiles/") if os.path.isdir(i)])


### --- COMMAND PARSING --- ###

def commandParser(COMMAND):
    # - NO COMMAND - #
    # No command given. Just go to 'info'.
    if not (COMMAND) or len(ARGS) < 2:
        COMMAND = 'info'

    # - INFO - #
    # Display banner and information.
    if COMMAND == 'info':
        with open('.info') as f:
            print(f.read())


    # - TEST - #
    # Test the CLI with an echo of the input.
    elif COMMAND == 'test':
        print('Test received! You typed in the CLI:')
        print(PARAMS)


    # - CREATE - #
    # Create new profile.
    elif COMMAND == 'create':
        if len(PARAMS) == 0:
            profile_id = str(n_profiles + 1)
        else:
            profile_id = PARAMS[0]
        print('Creating profile with ID: ' + profile_id)
        path = 'profiles/' + profile_id
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            raise FileExistsError('Chosen profile ID is already made.')
        log_file = open(path + '/log', '+w')
        info_file = open(path + '/info', '+w')
        log_file.close()
        info_file.close()
        utils.LOGFILE = path + '/log'
        os.makedirs(path + '/models/')
        os.makedirs(path + '/datasets/')
        log('Profile created.')


    # - DELETE - #
    # Delete a profile.
    elif COMMAND == 'delete':
        path = 'profiles/' + ARGS[1]
        shutil.rmtree(path)
        print("Profile " + ARGS[1] + " deleted.")


    # - DISTILL - #
    elif COMMAND == 'distill':
        if len(ARGS) < 4:
            raise ValueError('Missing arguments for distill.')
        profile_id = ARGS[1]
        model_from = ARGS[2]
        model_to = ARGS[3]
        model_env = ARGS[4]
        try:
            n_data = ARGS[5]
        except:
            n_data = 1000
        dis.distillation(model_from, model_to, model_env, profile_id, n_data)







    # - INVALID COMMAND - #
    # Command is not defined.
    else:
        raise NotImplementedError('Command ' + COMMAND + ' not available.')

commandParser(COMMAND)