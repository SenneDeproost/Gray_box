from torchvision import datasets, transforms
from structures.SoftDecisionTree.sdt.model import SoftDecisionTree
from torch.utils.data import TensorDataset, DataLoader
import torch
from Distillate import *
import numpy as np

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
    def new_model(self, args_file, args_dict=None):
        if self.type == 'ANT':
            pass
        if self.type == 'SDT':

            # Import args file
            import importlib.util
            spec = importlib.util.spec_from_file_location("args", args_file)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            parser = foo.parser
            args = parser.parse_args()
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

        # Get shapes input and output
        i_w = obs.shape[1]
        i_h = obs.shape[2]
        i_size = i_w * i_h


        # Transforms
        data_transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Lambda(torch.flatten)])

        target_transform = transforms.Lambda(
            lambda t: torch.as_tensor(torch.nn.functional.one_hot(torch.tensor(t), num_classes=self.args.output_dim), dtype=torch.float))

        obs = torch.flatten(obs, start_dim=1).to(torch.float)
        act = torch.nn.functional.one_hot(act.to(torch.int64), self.args.output_dim).flatten(start_dim=1).to(torch.float)

        dataset = TensorDataset(obs, act)
        trainset = TensorDataset(obs, act)

        train_loader = DataLoader(dataset, batch_size=self.args.batch_size, shuffle=True, **kwargs)
        test_loader = DataLoader(trainset, batch_size=self.args.batch_size, shuffle=True, **kwargs)

        model = self.model

        for epoch in range(1, self.args.epochs + 1):
            model.train_(train_loader, epoch)
            model.test_(test_loader, epoch)
