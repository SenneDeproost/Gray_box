import gym
from PIL import Image
import base64
import numpy as np
import cv2
from io import BytesIO
import json
import utils
from utils import log

env = None
model = None


# Load in new session // Todo: change models to distillates path
def load_session(profile, distillate, alg, environment):

    global env
    env = gym.make(environment)
    env.reset()
    #env.render()

    model = []
    alg = alg.upper()
    impo = 'from stable_baselines3 import {}'.format(alg)
    log('Loading learning algorithm.')
    exec(impo)
    log('Algorithm {} loaded.'.format(alg))
    model_path = 'profiles/{}/models/{}'.format(profile, distillate)
    ex = 'model.append({}.load(model_path, env=env, verbose=1))'.format(alg)
    log('Playing model {} in environment {}.'.format(distillate, env))
    exec(ex, locals())
    log('Model loaded.')
    global model
    model = model[0]

    rgb = env.render(mode='rgb_array')
    game_b64 = to_b64(rgb)
    data = {}
    data['game'] = game_b64.decode("utf-8")
    return data


# Do one step in the environment with model prediction as action.




# Convert RGB array to base 64.
def to_b64(array):
    img = Image.fromarray(array)
    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)
    return im_b64
