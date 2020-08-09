import sys
sys.path.append("/Users/senne/Thesis/Gray_box/structures/AdaptiveNeuralTrees")

from Visualizer import *
import torch
import torch.nn as nn
from torch.optim import Adam
from structures.AdaptiveNeuralTrees.utils import load_tree_model
from structures.SoftDecisionTree.sdt.model import SoftDecisionTree
from breakout_args import parser
import numpy as np
import matplotlib.pyplot as plt




# v = Visualizer("ANT")
# v.type
# #
# v.load_structure("tree_structures.json")
# print(v.tree)
# #v.show()
# v.load_model("model.pth")
#v.render_nodes(28, 28)
#v.show()
# w = list(model.tree_modules[15].classifier.fc.parameters())[1]
# print(w)

# q = Visualizer("ANT")
# q.load_model("model.pth")
# q.load_structure('tree_structures.json')
# q.build_tree()
# #q.render_nodes(28, 28)
# q.add_node_visuals()
# q.draw_path([0, 1, 3, 8, 14])
# q.show()
# q.draw_path([0, 2, 5, 11])
# q.show()
# print(q.tree)


q = Visualizer('SDT')
q.load_model('./.working/best.pt', 'breakout_args.py')
q.build_tree()
q.render_nodes(84, 84)
q.add_node_visuals()
q.show()
exit()




args = parser.parse_args()
args.device = torch.device('cpu')


d = SoftDecisionTree(args)
d.load_state_dict(torch.load('best.pt', map_location=torch.device(args.device)))
d.eval()

print(d.weights.shape)

w = d.weights[25]
w = w.detach().numpy()
w = w.reshape((84, 84))
plt.imshow(w, cmap='gray')
# plt.colorbar()
plt.xticks([])
plt.yticks([])
plt.show()


