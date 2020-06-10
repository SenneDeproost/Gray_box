import cloudpickle


class Distillate:
    def __init__(self, set):
        self.set = set

    # Save a dataset.
    def save(self, path):
        with open(path, '+wb') as f:
            data = cloudpickle.dumps(self.set)
            f.write(data)
            f.close()
        print('Distillate saved in ' + path + '.')

    # Load a dataset
    def load(self, path):
        with open(path, '+rb') as f:
            data = f.read()
            self.set = cloudpickle.loads(data)
            f.close()
        print('Distillate loaded from ' + path + '.')
