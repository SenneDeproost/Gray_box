import util
from util import log
import compress_pickle


class Distillate:
    def __init__(self, profile, model, type):
        self.profile = profile
        self.model = model
        self.type = type
        self.dataset_name = util.new_dataset_name(profile, model)
        self.path = 'profiles/{}/datasets/{}.{}'.format(profile, self.dataset_name, self.type)
        self.dataset = []

    # Save a dataset.
    def save(self):
        compress_pickle.to_gz_pickle(self.dataset, self.path)
        log('Distillate saved in {}.'.format(self.path))

    # Load a dataset
    def load(self, path):
        data = compress_pickle.read_gz_pickle(path)
        log('Distillate opened from {}.'.format(path))
        return data
