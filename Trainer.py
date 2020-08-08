
from structures.SoftDecisionTree.sdt.model import SoftDecisionTree
import torch

class Trainer:

    def __init__(self, type):
        self.type = type
        self.model = None

    # Load pytorch model
    def load_model(self, path, args=None):
        if self.type == 'ANT':
            pass
        if self.type == 'SDT':
            pass

    # Create new model
    def new_model(self, path, args_file, args_dict=None):
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

