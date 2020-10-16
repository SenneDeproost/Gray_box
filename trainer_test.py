from Trainer import *

# # Load SDT for MNIST
# t = Trainer('SDT')
# args = {}
#
# t.new_model('pong_args.py', args)
# t.train('Senne', 'PongNoFrameskip-v4_PPO_20000000_0_2500000')

from structures.AdaptiveNeuralTrees.ANT import AdaptiveNeuralTree

t = Trainer('SDT')
args = dict()
t.new_model('mspacman_args.py', args)
t.train('best', 'MsPacman-v0_PPO_20000000_1_100000')
exit()