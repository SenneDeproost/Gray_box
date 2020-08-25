from Distillate import *
import gym
from stable_baselines3.common.cmd_util import make_atari_env
import envlist
import cv2
import matplotlib.pyplot as plt

def distillation(profile, model_from, model_to, env, alg, distill_steps, epochs):
    from structures.SoftDecisionTree.sdt.model import SoftDecisionTree
    import torch
    from torch.utils.data import DataLoader, TensorDataset
    log('Distilling from model {} to model {} in environment {} for profile {}.'.format(model_from, model_to, env, profile))
    log('Generating {} entries in dataset.'.format(epochs))
    obs, act = record_experiences(profile, env, alg, distill_steps, model_from)

    log('Training model {} with dataset {}.'.format(model_to, obs.dataset_name))
    kwargs = {'num_workers': 1, 'pin_memory': True} if torch.cuda.is_available() else {}





    model = SoftDecisionTree(args)

    X = torch.tensor(obs)
    Y = torch.tensor(act)
    dataset = TensorDataset(X, Y)
    train_loader = DataLoader(dataset, batch_size=64, shuffle=True, **kwargs)
    for epoch in range(1, epochs + 1):
        model.train_(train_loader, epoch)
    return model






def record_experiences(profile, env_name, alg, steps, model_name):
    from stable_baselines3.common.atari_wrappers import AtariWrapper
    from baselines.common.retro_wrappers import WarpFrame
    recorded_obs = Distillate(profile, model_name, type='obs')
    recorded_act = Distillate(profile, model_name, type='act')

    model = []

    alg = alg.upper()
    impo = 'from stable_baselines3 import {}'.format(alg)
    log('Loading learning algorithm.')
    exec(impo)
    log('Algorithm {} loaded.'.format(alg))
    model_path = 'profiles/{}/models/{}'.format(profile, model_name)
    ex = 'model.append({}.load(model_path, env=env, verbose=1))'.format(alg)
    log('Playing model {} in environment {}.'.format(model_name, env_name))

    if env_name in envlist.atari:
        height, width = (105, 80)
        env = util.ThresholdWarpWrapper(gym.make(env_name), envlist.threshold[env_name], width, height)
        env.reset()

    exec(ex, locals())
    log('Model loaded.')
    model = model[0]

    # Play until the end
    log('Generating dataset.')
    obs = env.reset()

    stps = int(steps)
    for i in range(stps):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        if i % 8 in [0, 1, 2, 3]:
            #rec_obs = util.preprocess_obs(obs, envlist.threshold[env_name], width=width, height=height)
            rec_obs = obs
            recorded_obs.dataset.append(rec_obs)
            #import matplotlib.pyplot as plt
            #plt.imshow(rec_obs.reshape(84, 84), cmap='gray')
            #plt.show()
            recorded_act.dataset.append(action)
        if i % 1000 == 0:
            print('At step {}.'.format(i))
        if done:
            obs = env.reset()
    log('Closing environment.')
    env.close()

    recorded_obs.save()
    recorded_act.save()
    return recorded_obs, recorded_act
