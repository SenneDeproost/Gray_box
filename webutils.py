import os

# Return all profiles in a list.
def list_profiles():
    profiles = [dI for dI in os.listdir('profiles') if os.path.isdir(os.path.join('profiles',dI))]
    return profiles

def list_distillates(profile):
    path = 'profiles/{}/distillates'.format(profile)
    distillates = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path,dI))]
    return distillates
