from Trainer import *

# # Load SDT for MNIST
# t = Trainer('SDT')
# args = {}
#
# t.new_model('pong_args.py', args)
# t.train('Senne', 'PongNoFrameskip-v4_PPO_20000000_0_2500000')

t = Trainer('ANT')
args = dict()
t.new_model('pong_args_ant.py', args)