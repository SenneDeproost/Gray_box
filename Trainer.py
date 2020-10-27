from torchvision import datasets, transforms
from structures.SoftDecisionTree.sdt.model import SoftDecisionTree
from structures.AdaptiveNeuralTrees.ANT import AdaptiveNeuralTree
from torch.utils.data import TensorDataset, DataLoader
import torch
from Distillate import *
import numpy as np

from torchvision import datasets, transforms
from ops import ChunkSampler


class Trainer:

    def __init__(self, type):
        self.type = type
        self.model = None
        self.args = None

    # Load pytorch model
    def load_model(self, path, args=None):
        if self.type == 'ANT':
            pass
        if self.type == 'SDT':
            pass

    # Create new model
    def new_model(self, args_file, args_dict={}):

        # Import args file
        import importlib.util
        spec = importlib.util.spec_from_file_location("args", args_file)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        parser = foo.parser
        args, unknown = parser.parse_known_args()
        torch.manual_seed(args.seed)


        # CUDA
        args.cuda = not args.no_cuda and torch.cuda.is_available()
        if args.cuda:
            args.device = torch.device('cuda')
            if args.cuda_deterministic:
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
            print('Using GPU')
        else:
            args.device = torch.device('cpu')
            print('Using CPU')

        # Do arguments in args variable
        for key in args_dict.keys():
            value = args_dict[key]
            setattr(args, key, value)

        if self.type == 'ANT':
            # Create ANT
            model = AdaptiveNeuralTree(args)
            self.model = model
            self.args = args

        if self.type == 'SDT':
            # Create SDT
            model = SoftDecisionTree(args)
            self.model = model
            self.args = args




    def train(self, profile, model_name):

        kwargs = {'num_workers': 1, 'pin_memory': True} if self.args.cuda else {}

        # Load datasets
        obs = Distillate(profile, model_name, 'obs')
        act = Distillate(profile, model_name, 'act')
        obs.load('./profiles/{}/datasets/{}.obs'.format(profile, model_name))
        act.load('./profiles/{}/datasets/{}.act'.format(profile, model_name))
        obs = torch.from_numpy(np.array(obs.dataset))
        act = torch.from_numpy(np.array(act.dataset))



        n_data = len(obs)
        n_valid = 0.1 * n_data
        n_test = 0.05 * n_data
        idx_test = int(n_data - n_test)
        idx_valid = int(idx_test - n_valid)

        obs = torch.flatten(obs, start_dim=1).to(torch.float)
        if self.type == 'SDT':
            act = torch.nn.functional.one_hot(act.to(torch.int64)).flatten(start_dim=1).to(torch.float)
        elif self.type == 'ANT':
            act = act.to(torch.float)

        trainset = TensorDataset(obs[:idx_valid], act[:idx_valid])
        validset = TensorDataset(obs[idx_valid + 1: idx_test], act[idx_valid + 1:idx_test])
        testset = TensorDataset(obs[idx_test + 1:], act[idx_test + 1:])



        train_loader = DataLoader(trainset, batch_size=self.args.batch_size, shuffle=True, **kwargs)
        valid_loader = DataLoader(validset, batch_size=self.args.batch_size, shuffle=True, **kwargs)
        test_loader = DataLoader(testset, batch_size=self.args.batch_size, shuffle=True, **kwargs)


        model = self.model

        if self.type == 'SDT':

            for epoch in range(1, self.args.epochs + 1):
                model.train_(train_loader, epoch)
                model.test_(test_loader, epoch)

        if self.type == 'ANT':
            self.model.initialize(train_loader, valid_loader, test_loader, n_data, n_valid)
            self.model.grow_ant_nodewise()
