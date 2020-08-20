from Distillate import *
import gym
from stable_baselines3.common.cmd_util import make_atari_env
from stable_baselines3.common.atari_wrappers import AtariWrapper
import envlist
import sys
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from Distillate import *
import cv2



np.set_printoptions(threshold=sys.maxsize)

#env = AtariWrapper(gym.make('PongNoFrameskip-v4'))
env = gym.make('Enduro-v0')
#env = gym.make('Breakout-v4')
#env = make_atari_env('PongNoFrameskip-v4')
obs = env.reset()
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
env.step(1)
obs, _, _, _ = env.step(1)
print(obs)
env.render()

def preprocess(observation):
    observation = cv2.cvtColor(observation, cv2.COLOR_BGR2GRAY)
    #observation = cv2.adaptiveThreshold(observation,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    observation, th1 = cv2.threshold(observation, 50, 255, cv2.THRESH_BINARY)
    #observation, th3 = cv2.threshold(observation, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #return np.reshape(observation,(84,84))
    return th1

def preprocess(observation, threshold):
    observation = cv2.cvtColor(observation, cv2.COLOR_BGR2GRAY)
    observation, th1 = cv2.threshold(observation, threshold, 255, cv2.THRESH_BINARY)
    return th1

obs = preprocess(obs)
plt.imshow(obs, cmap='gray')
plt.show()
exit()


#recorded_act = Distillate('Senne', 'haha', type='act')
#recorded_act.load('./profiles/{}/datasets/{}.act'.format('Senne', 'PongNoFrameskip-v4_PPO_5000000_0_53336'))


pprint(obs, width=84, depth=84)

#print(obs.shape)
#print(recorded_act.dataset)
#plt.imshow(obs, cmap='gray')
#plt.show()