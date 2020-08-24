import arrow
import json
import time
import os
import cv2
import numpy as np


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
def new_dataset_name(profile, model, amount):
    #version = round((len([i.name for i in os.scandir("profiles/{}/datasets/".format(profile))]) - 0.1) / 2) # Some magic to make versions work
    name = '{}_{}'.format(model, amount)
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


# Preprocess the observation
    # Grayscale preprocess
def preprocess_obs(observation, thrshld, width, height):
    observation = observation.reshape(height, width)
    observation = cv2.cvtColor(observation, cv2.COLOR_GRAY2BGR)
    observation = cv2.cvtColor(observation, cv2.COLOR_BGR2GRAY)
    #observation, th1 = cv2.threshold(observation, thrshld, 255, cv2.THRESH_TOZERO)
    th1 = cv2.adaptiveThreshold(observation, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                cv2.THRESH_BINARY, 11, 2)
    #res = [1 if x == 255 else x for x in th1]
    #res = np.where(th1==255, 1, th1)
    #plt.imshow(th1, cmap='gray')
    #plt.show()
    #exit()
    return th1