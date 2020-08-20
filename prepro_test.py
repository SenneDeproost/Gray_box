import gym
from stable_baselines3.common.cmd_util import make_atari_env
import envlist
import cv2
import matplotlib.pyplot as plt
from stable_baselines3.common.atari_wrappers import AtariWrapper
from baselines.common.retro_wrappers import WarpFrame
import util


env = WarpFrame(gym.make('MsPacman-v0'), height=110, width=80)
obs = env.reset()
for i in range(100):
    obs = env.step(1)[0]



#obs = obs.reshape(110, 80)
obs = util.preprocess_obs(obs, thrshld=58, width=80, height=110)
t = plt.imshow(obs, cmap='gray')
#t.axes.get_xaxis().set_visible(False)
#t.axes.get_yaxis().set_visible(False)
#plt.axes.get_xaxis().set_visible(False)
#plt.axes.get_yaxis().set_visible(False)
#plt.imshow(obs)
plt.show()

