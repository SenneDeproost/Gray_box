import torch
from torch.utils.data import TensorDataset, DataLoader
from torchvision import datasets, transforms

from structures.SoftDecisionTree.args import parser
from structures.SoftDecisionTree.sdt.model import SoftDecisionTree
from Distillate import *

obs = Distillate('best', 6, 'obs')
act = Distillate('best', 6, 'act')
obs = obs.load('/Users/senne/Thesis/Gray_box/profiles/best/datasets/6_12.obs.gz')[0:5000]
obs = torch.as_tensor(obs)
act = act.load('/Users/senne/Thesis/Gray_box/profiles/best/datasets/6_12.act.gz')[0:5000]
act = torch.as_tensor(act)

args = parser.parse_args()
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

torch.manual_seed(args.seed)

kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}


data_transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Lambda(torch.flatten)])

target_transform = transforms.Lambda(
    lambda t: torch.as_tensor(torch.nn.functional.one_hot(torch.tensor(t), num_classes=4), dtype=torch.float))

print(obs.shape)
obs = torch.flatten(obs, start_dim=1).to(torch.float)
print(obs.shape)

act = torch.nn.functional.one_hot(act.to(torch.int64), 4).flatten(start_dim = 1).to(torch.float)








dataset = TensorDataset(obs[50:], act[50:])
trainset = TensorDataset(obs[0:50], act[0:50])

train_loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, **kwargs)
test_loader = DataLoader(trainset, batch_size=args.batch_size, shuffle=True, **kwargs)

soft_dec_tree = SoftDecisionTree(args)

for epoch in range(1, args.epochs + 1):
    soft_dec_tree.train_(train_loader, epoch)
    soft_dec_tree.test_(test_loader, epoch)

soft_dec_tree.save(args.save, 'final.pt')
print('Saved the final resulted model.')
