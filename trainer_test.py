from Trainer import *

# Load SDT for MNIST
t = Trainer('SDT')
args = {}

t.new_model('pong_args.py', args)
t.train('Senne', 'PongNoFrameskip-v4_PPO_2000_0_10000')