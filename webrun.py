import gym
from stable_baselines3.common.cmd_util import make_atari_env
from PIL import Image
import base64
import numpy as np
import cv2
from io import BytesIO
import json
import util
from util import log
import envlist

ENV = None
MODEL = None
OBS = None


# Load in new session // Todo: change models to distillates path
def load_session(profile, distillate, alg, environment, policy_type='"MlpPolicy"'):

    init = dict()

    ## Loading game
    if environment in envlist.atari:
        height, width = (105, 80)
        # env = EpisodicLifeEnv(gym.make(env_name))
        from stable_baselines3.common.monitor import Monitor
        # env = Monitor(AtariWrapper(gym.make(env_name)))
        # env = WarpFrame(gym.make(env_name), width=width, height=height, grayscale=True)
        env = util.ThresholdWarpWrapper(gym.make(environment), envlist.threshold[environment], width, height)
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


    ## Initial step in game
    global ENV
    ENV = env
    global MODEL
    MODEL = model

    rgb = env.render(mode='rgb_array')
    game_b64 = rgb_to_b64(rgb)
    init['game'] = game_b64.decode("utf-8")
    obs = env.reset()
    init['reward'] = "0"
    global OBS
    OBS = obs

    ## Tree visualisation
    path = "/Users/senne/Thesis/Gray_box/web/static/img/tree.svg"
    f = open(path, 'r')
    tree_data = f.read()
    init['tree'] = tree_data

    return init


# Do one step in the environment with model prediction as action.
def session_step():

    step = dict()

    ## Step in the game
    global OBS
    action, _states = MODEL.predict(OBS)
    OBS, reward, done, info = ENV.step(action)
    step['reward'] = str(reward)

    rgb = ENV.render(mode='rgb_array')
    game_b64 = rgb_to_b64(rgb)
    step['game'] = game_b64.decode("utf-8")
    if done:
        step['game'] = "done"

    ## Tree visualisation
    path = "/Users/senne/Thesis/Gray_box/web/static/img/tree.svg"
    f = open(path, 'r')
    tree_data = f.read()
    step['tree'] = tree_data

    return step


# Convert RGB array to base 64.
def rgb_to_b64(array):
    img = Image.fromarray(array)
    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)
    return im_b64
