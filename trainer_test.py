from Trainer import *

# Load SDT for MNIST
t = Trainer('SDT')
args = {}
args['depth'] = 7

t.new_model('best.pt', 'breakout_args.py', args)