import util
from util import log
#import stable_baselines3
import gym


def play(profile, env, alg, model_name):
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
def train_new(profile, env_name, alg, stps, policy_type='"MlpPolicy"'):
    # Preperation
    model = []
    log('Training new model with variables: \n  environment: {}\n  algorithm: {}\n  steps: {} \n  policy type: {}'.format(env, alg, stps, policy_type))
    alg = alg.upper()
    env = gym.make(env_name)
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
    model_name = util.new_model_name(profile)
    model_path = 'profiles/{}/models/{}'.format(profile, model_name)
    util.link_model(profile, model_name)
    util.link_env(profile, model_name, env_name)
    util.link_algorithm(profile, model_name, alg)
    log('Saving model to {}'.format(model_name))
    model.save(model_path)
    log('Model saved.')


# Create a new model and train it.
def train_loaded(profile, env, alg, stps, model_name, policy_type='"MlpPolicy"'):
    # Preperation
    model = []
    log('Training saved model with variables: \n environment: {}\n algorithm: {}\n steps: {} \n policy type: {} \n model: {}'.format(env, alg, stps, policy_type, model_name))
    alg = alg.upper()
    impo = 'from stable_baselines3 import {}'.format(alg)
    log('Loading learning algorithm.')
    exec(impo)
    log('Algorithm {} loaded.'.format(alg))
    model_path = 'profiles/{}/models/{}'.format(profile, model_name)
    ex = 'model.append({}.load(model_path, env=env, verbose=1))'.format(alg)
    env = gym.make(env)
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
