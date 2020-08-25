from stable_baselines3 import A2C
import gym
import util

env = gym.make('PongNoFrameskip-v4')
env = util.ThresholdWarpWrapper(env, 100, 80, 105)
model = A2C('MlpPolicy', env, verbose=2, tensorboard_log='./testje')
#print(model.env.unwrapped)
#print(model.env.observation([0]))
#print(model.env.observation.size)
model.env.reset()
print(model.observation_space)

# model.env.reset()
# exit()
#
# t = model.env.step([1])
# import matplotlib.pyplot as plt
# print(t)
# plt.imshow(t[0], cmap='gray')
# plt.show()
# exit()
model.learn(total_timesteps=20000, tb_log_name="second_run")