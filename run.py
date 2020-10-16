import util
from util import log
#import stable_baselines3
import gym
from stable_baselines3.common.cmd_util import make_atari_env
import envlist


def play(profile, env_name, alg, model_name):
    # Preperation
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
        env = gym.make(env_name)
        env = util.ThresholdWarpWrapper(env, 100, 80, envlist.threshold[env_name])
    exec(ex, locals())

    log('Model loaded.')
    model = model[0]

    # Play until the end
    obs = env.reset()
    for i in range(100000):
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            env.close()
            break
    log('Closing environment.')
    env.close()


# Create a new model and train it.
def train_new(profile, env_name, alg, stps, policy_type='"CnnPolicy"'):
    from stable_baselines3.common.atari_wrappers import WarpFrame, EpisodicLifeEnv, AtariWrapper
    from baselines.common.retro_wrappers import WarpFrame
    # Preperation
    model = []

    log('Training new model with variables: \n  environment: {}\n  algorithm: {}\n  steps: {} \n  policy type: {}'.format(env_name, alg, stps, policy_type))
    alg = alg.upper()
    if env_name in envlist.atari:
        height, width = (105, 80)
        #env = EpisodicLifeEnv(gym.make(env_name))
        from stable_baselines3.common.monitor import Monitor
        #env = Monitor(AtariWrapper(gym.make(env_name)))
        #env = WarpFrame(gym.make(env_name), width=width, height=height, grayscale=True)
        env = util.ThresholdWarpWrapper(gym.make(env_name), envlist.threshold[env_name], width, height)
        env.reset()
        # env.render()
        # obs = util.preprocess(obs, thrshld=envlist.threshold[env_name], width=width, height=height)
        # import matplotlib.pyplot as plt
        # plt.imshow(obs, cmap='gray')
        # plt.show()
        # exit()
    impo = 'from stable_baselines3 import {}'.format(alg)
    log('Loading learning algorithm.')
    exec(impo)

    log('Algorithm {} loaded.'.format(alg))
    tb_log = '"./profiles/{}/tensorboard"'.format(profile)
    ex = 'model.append({}({}, env, verbose=2, tensorboard_log={}))'.format(alg, policy_type, str(tb_log)) # Mlp- or CnnPolicy.
    exec(ex, locals())

    log('Model loaded.')
    model = model[0]

    model_name = util.new_model_name(profile, env_name, alg, stps)
    model_path = 'profiles/{}/models/{}'.format(profile, model_name)
    print(model_name)

    # Create empty zip file for representing the model in parallel model training
    with open(model_path + ".zip", "w+") as f:
        f.close()

    # Learn policy.
    log('Start training policy.')
    model.learn(total_timesteps=stps, tb_log_name=model_name)

    # Save model.
    log('Saving model to {}'.format(model_name))
    model.save(model_path)
    log('Model saved.')


# Create a new model and train it.
def train_loaded(profile, env_name, alg, stps, model_name, policy_type='"MlpPolicy"'):
    # Preperation
    model = []

    log('Training saved model with variables: \n environment: {}\n algorithm: {}\n steps: {} \n policy type: {} \n model: {}'.format(env_name, alg, stps, policy_type, model_name))
    alg = alg.upper()
    impo = 'from stable_baselines3 import {}'.format(alg)
    log('Loading learning algorithm.')
    exec(impo)

    log('Algorithm {} loaded.'.format(alg))
    model_path = 'profiles/{}/models/{}'.format(profile, model_name)
    ex = 'model.append({}.load(model_path, env=env, verbose=1))'.format(alg)
    if env_name in envlist:
        env = make_atari_env(env_name)
    exec(ex, locals())

    log('Model loaded.')
    model = model[0]

    # Learn policy.
    log('Start training policy.')
    model.learn(total_timesteps=stps)

    # Save model.
    model_name = util.new_model_name(profile)
    #utils.link_model(profile, model_name)
    #utils.link_env(profile, model_name, env)
    #utils.link_algorithm(profile, model_name, alg)
    log('Saving model to {}'.format(model_name))
    model.savemodel_(model_path)
    log('Model saved.')
