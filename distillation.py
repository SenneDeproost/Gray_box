import utils
from utils import log
from Distillate import *
import gym


def distillation(profile, model_from, model_to, env, alg, stps, trail_size):
    log('Distilling from model {} to model {} in environment {} for profile {}.'.format(model_from, model_to, env, profile))
    log('Generating {} entries in dataset.'.format(stps))


def record_experiences(profile, env, alg, stps, model_name):
    recorded_obs = Distillate(profile, model_name, typ='obs')
    recorded_act = Distillate(profile, model_name, typ='act')

    # Preperation
    model = []
    alg = alg.upper()
    impo = 'from stable_baselines3 import {}'.format(alg)
    log('Loading learning algorithm.')
    exec(impo)
    log('Algorithm {} loaded.'.format(alg))
    model_path = 'profiles/{}/models/{}'.format(profile, model_name)
    ex = 'model.append({}.load(model_path, env=env, verbose=1))'.format(alg)
    log('Playing model {} in environment {}.'.format(model_name, env))
    env = gym.make(env)
    exec(ex, locals())
    log('Model loaded.')
    model = model[0]

    # Play until the end
    log('Generating dataset.')
    obs = env.reset()
    for i in range(stps):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        if i % 60 in [0, 1, 2, 3]:
            recorded_obs.dataset.append(obs)
            recorded_act.dataset.append(action)
        if i % 1000 == 0:
            print('At step {}.'.format(i))
        if done:
            obs = env.reset()
    log('Closing environment.')
    env.close()

    recorded_obs.save()
    recorded_act.save()
    #utils.link_dataset(profile, model_name, recorded_obs.dataset_name) // Todo: Fix linkage

