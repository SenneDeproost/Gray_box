from stable_baselines3.common.cmd_util import make_atari_env
import gym
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3 import PPO

# There already exists an environment generator
# that will make and wrap atari environments correctly.
# Here we are also multi-worker training (n_envs=4 => 4 environments)
env = make_atari_env('BreakoutNoFrameskip-v4')

# model = PPO('CnnPolicy', env, verbose=1)
# model.learn(total_timesteps=100000)
#
# model.save("6")
env.reset()
model = PPO.load("6.zip", env, verbose=1)

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()