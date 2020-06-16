import utils
from utils import log
#import stable_baselines3
import gym
from importlib import import_module


def play(env, algorithm, episodes):
    env = gym.make(env)
    import_module(algorithm) # ToDo Change import
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


# Create a new model and train it.
def train_new(profile, env, alg, stps, policy_type='"MlpPolicy"'):
    # Preperation
    model = []
    log('Training new model with variables: \n environment: {}\n algorithm: {}\n steps: {} \n policy type: {}'.format(env, alg, stps, policy_type))
    alg = alg.upper()
    impo = 'from stable_baselines3 import {}'.format(alg)
    log('Loading learning algorithm.')
    exec(impo)
    log('Algorithm {} loaded.'.format(alg))
    ex = 'model.append({}({}, env, verbose=1))'.format(alg, policy_type) # Mlp- or CnnPolicy.
    exec(ex, locals())
    log('Model loaded.')
    model = model[0]

    # Learn policy.
    log('Start training policy.')
    model.learn(total_timesteps=stps)

    # Save model.
    model_name = utils.new_model_name(profile)
    path = 'profiles/{}/models/{}'.format(profile, model_name)
    utils.link_model(profile, model_name)
    utils.link_env(profile, model_name, env)
    utils.link_algorithm(profile, model_name, alg)
    log('Saving model to {}'.format(model_name))
    model.save(path)
    log('Model saved.')