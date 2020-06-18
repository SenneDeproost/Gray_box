import cloudpickle
import utils
from utils import log


class Distillate:
    def __init__(self, profile, model):
        self.profile = profile
        self.model = model
        self.dataset_name = utils.get_dataset_name(profile, model)
        self.path = 'profiles/{}/datasets/{}'.format(model, self.dataset_name)

    # Save a dataset.
    def save(self):
        with open(self.path, '+wb') as f:
            data = cloudpickle.dumps(self.set)
            f.write(data)
            f.close()
        log('Distillate saved in {}.'.format(self.dataset_name))

    # Load a dataset
    def load(self, path):
        with open(path, '+rb') as f:
            data = f.read()
            self.set = cloudpickle.loads(data)
            f.close()
        log('Distillate saved in {}.'.format(self.dataset_name))
