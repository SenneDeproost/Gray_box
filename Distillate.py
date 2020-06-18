import utils
from utils import log
import compress_pickle


class Distillate:
    def __init__(self, profile, model, typ, compressed=False):
        self.profile = profile
        self.model = model
        self.typ = typ
        self.dataset_name = utils.new_dataset_name(profile, model)
        self.path = 'profiles/{}/datasets/{}.{}'.format(profile, self.dataset_name, self.typ)
        self.dataset = []
        self.compressed = compressed

    # Save a dataset.
    def save(self):
        compress_pickle.to_gz_pickle(self.dataset, self.path)
        log('Distillate saved in {}.'.format(self.path))

    # Load a dataset
    def load(self, path):
        data = compress_pickle.read_gz_pickle(path)
        log('Distillate opened from {}.'.format(path))
        return data
