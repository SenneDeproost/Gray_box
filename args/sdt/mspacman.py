import argparse
import pickle
import util
import time
time = str(round(time.time()))

save_dir = str(util.DATASET_NAME) + "_" + "SDT" + "_" + time
save_dir = "./profiles/{}/distillates/{}".format(util.PROFILE_NAME, save_dir)

parser = argparse.ArgumentParser(description='Soft Decision Tree')
# Model args
parser.add_argument('--batch-size', type=int, default=64, help='input batch size for training (default: 64)')
parser.add_argument('--input-dim', type=int, default=105*80, help='input dimension size(default: 784 --> 7056)')
parser.add_argument('--output-dim', type=int, default=6, help='output dimension size (default: 10)')
parser.add_argument('--depth', type=int, default=4, help='Depth of tree (default: 5)')
parser.add_argument('--lmbda', type=float, default=0.1, help='penalty strength rate (default: 0.1)')
# Training args
parser.add_argument('--root', type=str, default=".", help="Folder of MNIST dataset")
parser.add_argument('--epochs', type=int, default=20, help='number of epochs to train (default: 20)')
parser.add_argument('--no-cuda', action='store_true', default=False, help='disables CUDA training')
# Reproducability
parser.add_argument('--seed', type=int, default=1, help='random seed (default: 1)')
parser.add_argument('--cuda-deterministic', action='store_true', default=False,
                    help="sets flags for determinism when using CUDA (potentially slow!)")
# Logging
parser.add_argument('--log-interval', type=int, default=20,
                    help='how many batches to wait before logging training status')
parser.add_argument('--save', default=save_dir, help='Folder to save trained models')
parser.add_argument('--tensorboard', action='store_true', default=True, help='Tensorboard logging')

# Dataset
parser.add_argument('--dataset', type=str, default='mnist', help='Name of the dataset')
parser.add_argument('--augmentation_on', type=bool, default=False, help='Augmentation of dataset')