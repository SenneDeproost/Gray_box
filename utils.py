import arrow
import json
import time
import os


LOGFILE = None

# Print the output in stdout + log in log file.
def log(text):
    print(text)
    timestamp = arrow.get().format('DD-MMM-YYYY HH:mm:ss')
    if LOGFILE:
        with open(LOGFILE, 'a') as f:
            f.write(timestamp + ' - ' + text.replace('\n',''))
            f.write("\n")
   # else:
        #raise FileNotFoundError('LOGFILE variable not assigned.')


# Load profile info file into memory.
def load_info(profile):
    path = "./profiles/{}/info".format(profile)
    with open(path, 'r') as f:
        data = json.load(f)
        f.close()
        return data


# Save profile info file from memory.
def save_info(profile, data):
    path = "./profiles/{}/info".format(profile)
    with open(path, '+w') as f:
        json.dump(data, f)
        f.close()


# Generate new model name.
def new_model_name(profile):
    name = str(len(load_info(profile)))
    return name


# Generate name for new dataset.
def new_dataset_name(profile, model):
    datasets = [i.name for i in os.scandir("profiles/{}/datasets/".format(profile))]
    indx = len(datasets)
    name = '{}_{}'.format(model, indx)
    return name

# Get model with model name.
def get_model(profile, model):
    f = load_info(profile)
    for i in range(0, len(f)):
        m = f[i]
        if m['model'] == model:
            return i


# Initialize the info file for a profile.
def init_info(profile):
    data = []
    save_info(profile, data)


# Add model to the profile info file.
def link_model(profile, model):
    f = load_info(profile)
    keys = ['model', 'dataset', 'environment', 'algorithm']
    data = {key: [] for key in keys}
    data['model'] = model
    f.append(data)
    save_info(profile, f)


# Link dataset to model.
def link_dataset(profile, model, dataset):
    f = load_info(profile)
    i = get_model(profile, model)
    data = f[i]
    data['dataset'].append(dataset)
    f[i] = data
    save_info(profile, f)


# Link environment to model.
def link_env(profile, model, env):
    f = load_info(profile)
    i = get_model(profile, model)
    data = f[i]
    data['environment'] = env
    f[i] = data
    save_info(profile, f)


# Link algorithm to model.
def link_algorithm(profile, model, alg):
    f = load_info(profile)
    i = get_model(profile, model)
    data = f[i]
    data['algorithm'] = alg
    f[i] = data
    save_info(profile, f)
