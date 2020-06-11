import utils
from utils import log
import gym


def distillation(model_from, model_to, env, profile, n_data=1000):
    log('Distilling from model {} to model {} in environment {} for profile {}.'.format(
        model_from, model_to, env, profile
    ))
    log('Generating {} entries in dataset.'.format(n_data))

    env = gym.make(env)

