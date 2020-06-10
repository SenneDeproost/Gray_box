import utils
from utils import log



def distillation(model_from, model_to, env, profile, n_data=1000):
    profile_path = 'profiles/' + profile
    utils.LOGFILE = profile_path + '/log'
    log('Distilling from model {} to model {} in environment {} for profile {}.'.format(
        model_from, model_to, env, profile
    ))
    log('Generating {} entries in dataset.'.format(n_data))

