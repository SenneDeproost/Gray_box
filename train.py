from Trainer import *
import util
from util import log

def train(profile, dataset, args_file, model_to):

    trainer = Trainer(model_to)
    args = dict()
    trainer.new_model(args_file, args)
    trainer.train(profile, dataset)