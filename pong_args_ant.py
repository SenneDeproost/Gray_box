import argparse

# Experiment settings
parser = argparse.ArgumentParser(description='Adaptive Neural Trees')
parser.add_argument('--experiment', '-e', dest='experiment', default='tree', help='experiment name')
parser.add_argument('--subexperiment','-sube', dest='subexperiment', default='', help='experiment name')

parser.add_argument('--dataset', default='mnist', help='dataset type')
parser.add_argument('--no-cuda', action='store_true', default=False, help='disables CUDA training')
parser.add_argument('--gpu', type=str, default="", help='which GPU to use')
parser.add_argument('--seed', type=int, default=0, metavar='S', help='random seed')
parser.add_argument('--num_workers', type=int, default=0, metavar='N', help='number of threads for data-loader')

# Optimization settings:
parser.add_argument('--batch-size', type=int, default=64, metavar='N', help='input batch size for training')
parser.add_argument('--log-interval', type=int, default=10, metavar='N', help='how many batches to wait before logging training status')
parser.add_argument('--augmentation_on', action='store_true', default=False, help='perform data augmentation')
parser.add_argument('--lr', type=float, default=0.001, metavar='LR', help='learning rate')
parser.add_argument('--scheduler', type=str, default="", help='learning rate scheduler')
parser.add_argument('--momentum', type=float, default=0.5, metavar='M', help='SGD momentum')
parser.add_argument('--valid_ratio', '-vr', dest='valid_ratio', type=float, default=0.1, metavar='LR', help='validation set ratio')

parser.add_argument('--criteria', default='avg_valid_loss', help='growth criteria')
parser.add_argument('--epochs_node', type=int, default=500, metavar='N', help='max number of epochs to train per node during the growth phase')
parser.add_argument('--epochs_finetune', type=int, default=100, metavar='N', help='number of epochs for the refinement phase')
parser.add_argument('--epochs_patience', type=int, default=5, metavar='N', help='number of epochs to be waited without improvement at each node during the growth phase')
parser.add_argument('--maxdepth', type=int, default=10, help='maximum depth of tree')
parser.add_argument('--finetune_during_growth', action='store_true', default=False, help='refine the tree globally during the growth phase')
parser.add_argument('--epochs_finetune_node', type=int, default=50, metavar='N', help='number of epochs to perform global refinement at each node during the growth phase')


# Solver, router and transformer modules:
parser.add_argument('--router_ver', '-r_ver', dest='router_ver', type=int, default=4, help='default router version')
parser.add_argument('--router_ngf', '-r_ngf', dest='router_ngf', type=int, default=1, help='number of feature maps in routing function')
parser.add_argument('--router_k', '-r_k', dest='router_k', type=int, default=28, help='kernel size in routing function')
parser.add_argument('--router_dropout_prob', '-r_drop', dest='router_dropout_prob', type=float, default=0.0, help='drop-out probabilities for router modules.')

parser.add_argument('--transformer_ver', '-t_ver', dest='transformer_ver', type=int, default=1, help='default transformer version: identity')
parser.add_argument('--transformer_ngf', '-t_ngf', dest='transformer_ngf', type=int, default=3, help='number of feature maps in residual transformer')
parser.add_argument('--transformer_k', '-t_k', dest='transformer_k', type=int, default=5, help='kernel size in transfomer function')
parser.add_argument('--transformer_expansion_rate', '-t_expr', dest='transformer_expansion_rate', type=int, default=1, help='default transformer expansion rate')
parser.add_argument('--transformer_reduction_rate', '-t_redr', dest='transformer_reduction_rate', type=int, default=2, help='default transformer reduction rate')

parser.add_argument('--solver_ver', '-s_ver', dest='solver_ver', type=int, default=1, help='default router version')
parser.add_argument('--solver_inherit', '-s_inh', dest='solver_inherit',  action='store_true', help='inherit the parameters of the solver when defining two new ones for splitting a node')
parser.add_argument('--solver_dropout_prob', '-s_drop', dest='solver_dropout_prob', type=float, default=0.0, help='drop-out probabilities for solver modules.')

parser.add_argument('--downsample_interval', '-ds_int', dest='downsample_interval', type=int, default=0, help='interval between two downsampling operations via transformers i.e. 0 = downsample at every transformer')
parser.add_argument('--batch_norm', '-bn', dest='batch_norm', action='store_true', default=False, help='turn batch norm on')

# Visualisation:
parser.add_argument('--visualise_split', action='store_true', help='visuliase how the test dist is split by the routing function')


# Extra
parser.add_argument('--input-dim', type=int, default=105*80, help='input dimension size(default: 784 --> 7056)')
parser.add_argument('--output-dim', type=int, default=6, help='output dimension size (default: 10)')
parser.add_argument('--depth', type=int, default=5 , help='Depth of tree (default: 5)')
parser.add_argument('--lmbda', type=float, default=0.1, help='penalty strength rate (default: 0.1)')
parser.add_argument('--input_nc', type=int, default=1, help='Number of chanels in input')
parser.add_argument('--input_width', type=int, default=80, help='Input width')
parser.add_argument('--input_height', type=int, default=105, help='Input height')
parser.add_argument('--classes', default=(0, 1, 2, 3, 4, 5))
parser.add_argument('--no_classes', default=6)
