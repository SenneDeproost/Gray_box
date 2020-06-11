import os
import shutil
import sys

import utils
from utils import log
import distillation as dis

### --- PREPARATON --- ###

global PROFILE
with open('.profile') as f:
    PROFILE = f.read()

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

if not os.path.exists('profiles'):
    os.makedirs('profiles')

PROFILES = [i.name for i in os.scandir("./profiles/") if os.path.isdir(i)]
n_profiles = len(PROFILES)

# Program execution without command.
if not COMMAND or len(PARAMS) == 0:
    COMMAND = 'info'

# Use the currently set profile when none is given.
elif not(PARAMS[0] in PROFILES) and not(COMMAND.startswith('profile-')):
    PARAMS.insert(0, PROFILE)




### --- COMMAND PARSING --- ###

def commandParser(command, params):
    # - NO COMMAND - #
    # No command given. Just go to 'info'.
    if not (command) or len(params) < 1:
        command = 'info'


    # - INFO - #
    # Display banner and information.
    if command in ('info', 'help'):
        with open('.info') as f:
            print(f.read())


    # - TEST - #
    # Test the CLI with an echo of the input.
    elif command == 'test':
        print('Test received! You typed in the CLI:')
        print(params)


    # - CREATE - #
    # Create new profile.
    elif command == 'profile-create':
        if len(params) == 0:
            profile_id = str(n_profiles + 1)
        else:
            profile_id = params[0]
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
        log('Profile ' + profile_id + ' created.')


    # - DELETE - #
    # Delete a profile.
    elif command == 'profile-delete':
        profile_id = params[0]
        path = 'profiles/' + profile_id
        shutil.rmtree(path)
        print("Profile " + profile_id + " deleted.")

    # - PROFILE-SET - #
    # Set the profile variable.
    #elif

    # - DISTILL - #
    elif command == 'distill':
        if len(ARGS) < 3:
            raise ValueError('Missing arguments for distill.')
        profile_id = params[0]
        model_from = params[1]
        model_to = params[2]
        model_env = params[3]
        try:
            n_data = params[4]
        except:
            n_data = 1000
        profile_path = 'profiles/' + profile_id
        utils.LOGFILE = profile_path + '/log'
        dis.distillation(model_from, model_to, model_env, profile_id, n_data)


    # - TRAIN - #
    elif command == 'train':
        profile_id = params[0]
        env = params[1]
        alg = params[2]






    # - INVALID COMMAND - #
    # Command is not defined.
    else:
        raise NotImplementedError('Command ' + COMMAND + ' not available.')

commandParser(COMMAND, PARAMS)