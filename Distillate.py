import util
from util import log
import compress_pickle


class Distillate:
    def __init__(self, profile, model, type):
        self.profile = profile
        self.model = model
        self.type = type
        self.dataset = []

    # Save a dataset.
    def save(self):
        amount = len(self.dataset)
        dataset_name = util.new_dataset_name(self.profile, self.model, amount)
        path = 'profiles/{}/datasets/{}.{}'.format(self.profile, dataset_name, self.type)
        compress_pickle.dump(self.dataset, path, compression="gzip", set_default_extension=False)
        log('Distillate saved in {}.'.format(path))

    # Load a dataset
    def load(self, path):
        data = compress_pickle.load(path, compression="gzip", set_default_extension=False)
        log('Distillate opened from {}.'.format(path))
        self.dataset = data
        return data
