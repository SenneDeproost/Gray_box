from stable_baselines3.common.cmd_util import make_atari_env
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from util import ThresholdWarpWrapper
import gym

env = gym.make('PongNoFrameskip-v4')
env = ThresholdWarpWrapper(env, 110, 80, 105)
#env = Monitor(env)

model = PPO('CnnPolicy', env, verbose=1)
model.learn(total_timesteps=2000000)

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()