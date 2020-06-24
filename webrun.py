import gym
from stable_baselines3.common.cmd_util import make_atari_env
from PIL import Image
import base64
import numpy as np
import cv2
from io import BytesIO
import json
import utils
from utils import log

ENV = None
MODEL = None
OBS = None


# Load in new session // Todo: change models to distillates path
def load_session(profile, distillate, alg, environment, policy_type='"CnnPolicy"'):

    env = make_atari_env(environment)
    env.reset()

    model = []
    alg = alg.upper()
    impo = 'from stable_baselines3 import {}'.format(alg)
    log('Loading learning algorithm.')
    exec(impo)
    log('Algorithm {} loaded.'.format(alg))
    model_path = 'profiles/{}/models/{}'.format(profile, distillate)
    ex = 'model.append({}.load(model_path, env, verbose=1))'.format(alg)
    log('Playing model {} in environment {}.'.format(distillate, environment))
    exec(ex, locals())
    log('Model loaded.')
    model = model[0]



    global ENV
    ENV = env
    global MODEL
    MODEL = model

    rgb = env.render(mode='rgb_array')
    game_b64 = to_b64(rgb)
    data = {}
    data['game'] = game_b64.decode("utf-8")
    obs = env.reset()
    global OBS
    OBS = obs
    return data


# Do one step in the environment with model prediction as action.
def session_step():
    global OBS
    action, _states = MODEL.predict(OBS)
    OBS, reward, done, info = ENV.step(action)

    rgb = ENV.render(mode='rgb_array')
    game_b64 = to_b64(rgb)
    data = {}
    data['game'] = game_b64.decode("utf-8")
    if done:
        data['game'] = "done"
    return data


# Convert RGB array to base 64.
def to_b64(array):
    img = Image.fromarray(array)
    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)
    return im_b64
