from Distillate import *
import gym
from stable_baselines3.common.cmd_util import make_atari_env
from stable_baselines3.common.atari_wrappers import AtariWrapper
from baselines.common.retro_wrappers import WarpFrame
import envlist
import sys
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from Distillate import *
import cv2
from stable_baselines3 import PPO
import util
import matplotlib.pyplot as plt

env_name = 'SpaceInvaders-v0'
height, width = (105, 80)
env = WarpFrame(gym.make(env_name), width=width, height=height, grayscale=True)
profile = 'Senne'
model_name = env_name + "_PPO_20000000_0"
model = PPO.load("./profiles/{}/models/{}.zip".format(profile, model_name))

obs = env.reset()
#obs = util.preprocess_obs(obs, thrshld=envlist.threshold[env_name], width=160, height=210)
#plt.imshow(obs, cmap='gray')
#plt.show()

for i in range(100000):
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    #obs = util.preprocess_obs(obs, thrshld=envlist.threshold[env_name], width=80, height=105)
    env.render()
    if done:
        env.close()
        break
