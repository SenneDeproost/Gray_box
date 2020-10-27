from Trainer import *

# # Load SDT for MNIST
# t = Trainer('SDT')
# args = {}
#
# t.new_model('pong_args.py', args)
# t.train('Senne', 'PongNoFrameskip-v4_PPO_20000000_0_2500000')

from structures.AdaptiveNeuralTrees.ANT import AdaptiveNeuralTree

t = Trainer('ANT')
args = dict()
t.new_model('pong_args_ant.py', args)
t.train('best', 'PongNoFrameskip-v4_PPO_20000000_1_500000')
exit()

t = Trainer('SDT')
args = dict()
t.new_model('pong_args.py', args)
t.train('best', 'PongNoFrameskip-v4_PPO_20000000_1_40000')
exit()


