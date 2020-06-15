import utils
from utils import log
#import stable_baselines3
import gym
from importlib import import_module


def play(env, algorithm, episodes):
    env = gym.make(env)
    import_module(algorithm)
    model_class = eval(algorithm)
    model = model_class('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=episodes)

    obs = env.reset()
    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()

    env.close()

def train_new(profile, env, alg, eps):

    pass
