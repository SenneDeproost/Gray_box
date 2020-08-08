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
def new_model_name(profile, env, alg, stps):
    base_name = "{}_{}_{}".format(env, alg, stps)
    version = 0
    for f in os.listdir("./profiles/{}/models".format(profile)):
        if f.startswith(base_name):
            version += 1
    model_name = "{}_{}".format(base_name, version)
    return model_name


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