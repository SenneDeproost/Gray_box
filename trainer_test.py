from Trainer import *

# Load SDT for MNIST
t = Trainer('SDT')
args = {}
args['depth'] = 5

t.new_model('breakout_args.py', args)
t.train('Senne', 'PongNoFrameskip-v4_PPO_5000000_0_53336')