import os
import shutil
import sys

import util
from util import log
import distillation as dis
import run
import subprocess


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

if not os.path.exists('.working'):
    os.makedirs('.working')

PROFILES = [i.name for i in os.scandir("profiles/") if os.path.isdir(i)]

# Program execution without command.
if not COMMAND: #or len(PARAMS) == 0:
    COMMAND = 'info'

# Use the currently set profile when none is given.
elif PARAMS:
    if not(PARAMS[0] in PROFILES) and not(COMMAND.startswith('profile-')):
        PARAMS.insert(0, PROFILE)

### --- COMMAND PARSING --- ###

def commandParser(command, params):

    # The log variable for profile and count number of params.
    if len(params) > 0:
        profile = params[0]
        profile_path = 'profiles/' + profile
        util.LOGFILE = profile_path + '/log'
    n_params = len(params)

    # - NO COMMAND - #
    # No command given. Just go to 'info'.
    if not (command): #or n_params < 1:
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
        if n_params == 1:
            profile = params[0]
        else:
            raise ValueError('Incorrect amount of parameters given for {} command.'.format(command))
        print('Creating profile with ID: ' + profile)
        path = 'profiles/' + profile
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            raise FileExistsError('Chosen profile ID is already made.')
        log_file = open(path + '/log', '+w')
        log_file.close()
        util.LOGFILE = path + '/log'
        os.makedirs(path + '/models/')
        os.makedirs(path + '/datasets/')
        os.makedirs(path + '/distillates/')
        util.init_info(profile)
        log('Profile ' + profile + ' created.')

    # - DELETE - #
    # Delete a profile.
    elif command == 'profile-delete':
        shutil.rmtree(profile_path)
        print("Profile " + profile_path + " deleted.")

    # - PROFILE-SET - #
    # Set the profile variable.
    elif command == 'profile-set':
        new_profile_id = params[0]
        with open('.profile', '+w') as f:
            f.write(new_profile_id)
            f.close()
        print('Profile set to {}.'.format(new_profile_id))

    # - DISTILL - # /// Todo: implementing distill + change params position
    elif command == 'distill':
        model_from = params[1]
        model_to = params[2]
        model_env = params[3]
        if len(params) == 4:
            n_data = params[4]
            dis.distillation(model_from, model_to, model_env, profile, n_data)
        elif len(params) == 3:
            dis.distillation(model_from, model_to, model_env, profile)
        else:
            raise ValueError('Incorrect amount of parameters given for {} command.'.format(command))

    # - PLAY - #
    elif command == 'play':
        if n_params == 4:
            profile, env, alg, model = params
            res = run.play(profile, env, alg, model)
        else:
            raise ValueError('Incorrect amount of parameters given for {} command.'.format(command))

    # - GENERATE - #
    # Generate a new dataset for distillation from model.
    elif command == 'generate':
        if n_params == 5:
            profile, env, alg, model, steps = params
            dis.record_experiences(profile, env, alg, steps, model)
        else:
            raise ValueError('Incorrect amount of parameters given for {} command.'.format(command))

    # - TRAIN - #
    elif command == 'train': # /// Todo: implement train_from_distillate
        if n_params == 4:
            profile, env, alg, stps = params
            res = run.train_new(profile, env, alg, int(stps))
            return res
        elif n_params == 5:
            profile, env, alg, stps, model = params
            res = run.train_loaded(profile, env, alg, int(stps), model)
        elif '--from_distillate' in params:
            params.remove('--from_distillate')
            profile, env, alg, stps, model = params
            #res = run.train_from_distillate(profile, env, alg, int(stps), model)
        else:
            raise ValueError('Incorrect amount of parameters given for {} command.'.format(command))

    #- WEB -#
    elif command == 'web':
        import web.app as webapp
        os.chdir('./Gray_box/')
        if len(params) == 0:
            webapp.app.run()
        else:
            raise ValueError('Incorrect amount of parameters given for {} command.'.format(command))





    # - INVALID COMMAND - #
    # Command is not defined.
    else:
        raise NotImplementedError('Command ' + command + ' not available.')

commandParser(COMMAND, PARAMS)
