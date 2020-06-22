import os


# Return all profiles in a list.
def list_profiles():
    profiles = [dI for dI in os.listdir('profiles') if os.path.isdir(os.path.join('profiles',dI))]
    return profiles


# Return list of all distillates in profile.
def list_distillates(profile):
    path = 'profiles/{}/distillates'.format(profile)
    distillates = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path,dI))]
    return distillates


# List all possible algorithms.
def list_algorithms():
    list = [
        'PPO',
        'A2C',
        'SAC',
        'TD3'
    ]
    return list