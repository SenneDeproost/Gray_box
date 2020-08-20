import gym
from stable_baselines3.common.cmd_util import make_atari_env
import envlist
import cv2
import matplotlib.pyplot as plt
from stable_baselines3.common.atari_wrappers import AtariWrapper
from baselines.common.retro_wrappers import WarpFrame
import util


env = WarpFrame(gym.make('Enduro-v0'), height=210, width=160)
obs = env.reset()
for i in range(100):
    obs = env.step(1)[0]



#obs = obs.reshape(210, 160)
obs = util.preprocess_obs(obs, thrshld=100, width=160, height=210)
t = plt.imshow(obs, cmap='gray')
t.axes.get_xaxis().set_visible(False)
t.axes.get_yaxis().set_visible(False)
#plt.axes.get_xaxis().set_visible(False)
#plt.axes.get_yaxis().set_visible(False)
#plt.imshow(obs)
plt.show()

