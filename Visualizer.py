import sys

sys.path.append("./structures/AdaptiveNeuralTrees")

from structures.AdaptiveNeuralTrees.utils import load_tree_model
from structures.SoftDecisionTree.sdt.model import SoftDecisionTree
import structures.SoftDecisionTree.args as sdt_args
import matplotlib.pyplot as plt

import torch.nn as nn

import json

import numpy as np

import queue

import torch

from ete3 import Tree, TreeStyle, add_face_to_node, TextFace, ImgFace


class Visualizer:

    def __init__(self, type):
        self.type = type
        self.structure = None
        self.tree = Tree()
        self.ts = TreeStyle()
        self.init_ts()
        self.model = None
        self.leafs = []
        self.paths = []
        self.class_paths = []
        self.path_starts = []
        self.distributions = []

    # Load structure file into class
    def load_structure(self, path):
        with open(path, 'r') as f:
            self.structure = json.load(f)
            if self.type == 'ANT':
                self.build_ant()
            f.close()

    # Load model pytorch model
    def load_model(self, path, args=None, extra_args=None):
        if self.type == "ANT":
            self.model = load_tree_model(path)
        if self.type == "SDT":

            # Import args file
            import importlib.util
            spec = importlib.util.spec_from_file_location("args", args)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            parser = foo.parser
            args = parser.parse_args()

            # CUDA
            args.cuda = not args.no_cuda and torch.cuda.is_available()
            if args.cuda:
                args.device = torch.device('cuda')
                if args.cuda_deterministic:
                    torch.backends.cudnn.deterministic = True
                    torch.backends.cudnn.benchmark = False
                print('Using GPU')
            else:
                args.device = torch.device('cpu')
                print('Using CPU')

            # Do arguments in args variable
            for key in extra_args.keys():
                value = extra_args[key]
                setattr(args, key, value)

            # Load SDT
            model = SoftDecisionTree(args)
            model.load_state_dict(torch.load(path, map_location=torch.device(args.device)))
            model.eval()
            self.model = model

    # Build tree
    def build_tree(self):
        if self.type == "ANT":
            self.build_ant()
        if self.type == "SDT":
            self.build_sdt()

    # Build up ete3 Tree SDT structure
    def build_sdt(self):
        # Calculate the height of the binary structure
        n_nodes = self.model.weights.shape[0]
        counter = 1
        height = 0
        while (counter < n_nodes + 1):
            counter *= 2
            height += 1

        # Build up tree
        self.tree = Tree("(0);")
        q = queue.Queue()
        q.put(self.tree.children[0])
        node_counter = 1
        while node_counter < n_nodes:
            # 1
            node = q.get()
            child_name = str(node_counter)
            node.add_child(name=child_name)
            child_node = self.tree.search_nodes(name=child_name)[0]
            q.put(child_node)
            node_counter += 1
            # 2
            child_name = str(node_counter)
            node.add_child(name=child_name)
            child_node = self.tree.search_nodes(name=child_name)[0]
            q.put(child_node)
            node_counter += 1

        # Calc leaf nodes range
        leafs = range((2**(height - 1)) - 1 , (2**height) - 1) #!!!!!!
        for leaf in leafs:
            self.leafs.append(str(leaf))
        print(leafs)


    # Build up ete3 Tree ANT structure
    def build_ant(self):
        # The root node
        root = self.structure[0]
        root_index = root['index']
        self.tree = Tree("(0);")
        self.tree.name = 0
        # self.tree.add_child(name=str(root_index))

        q = queue.Queue()
        q.put(self.tree.children[0])

        # Rest of the nodes
        while not q.empty():
            node = q.get()
            name = node.name
            indx = int(name)
            struct = self.structure[indx]

            parent = struct['parent']
            left_child = struct['left_child']
            right_child = struct['right_child']
            is_leaf = struct['is_leaf']
            index = struct['index']

            # Stop at leaf node
            if is_leaf and not node.name in self.leafs:
                self.leafs.append(node.name)


            else:
                # Internal node with children
                left_name = str(left_child)
                right_name = str(right_child)
                if not left_name == "0":
                    node.add_child(name=left_name)
                if not right_name == "0":
                    node.add_child(name=right_name)
                children = node.children
                for child in children:
                    q.put(child)

    # Show tree with correct layout
    def show(self):
        self.tree.show(tree_style=self.ts)

    def save(self, path):
        self.tree.render("{}.svg".format(path), tree_style=self.ts)

    # Initialize layout
    def init_ts(self):
        ts = self.ts
        ts.rotation = 90
        ts.show_leaf_name = False
        ts.show_scale = False

        # def my_layout(node):
        #
        #     if not 'dist' in str(value):
        #         F2 = TextFace(str(value), tight_text=True, fsize=30)
        #         F2.rotation = -90
        #         add_face_to_node(F2, node, column=0, position="branch-right")
        #
        #         #F = TextFace(node.name, tight_text=True)
        #         #F.rotation = -90
        #         #add_face_to_node(F, node, column=0, position="branch-right")
        #
        # ts.layout_fn = layout

    # Visualize node weights
    def render_nodes(self, width, height):
        wdir = "./.working/"

        # ANT
        if self.type == "ANT":
            modules = self.model.tree_modules
            self.distributions = [[]] * len(modules)
            for i in range(len(modules)):
                w = list(modules[i].classifier.fc.parameters())[0] # Router????
                w = w.detach().numpy()
                n_classes, input_size = w.shape
                t = np.zeros(input_size)

                for a in range(input_size):
                    for b in range(n_classes):
                        t[a] += w[b][a]

                t = t.reshape(width, height)
                plt.clf()
                plt.imshow(t, cmap='gray')
                # plt.colorbar()
                plt.xticks([])
                plt.yticks([])
                # plt.show()
                plt.savefig("{}{}.svg".format(wdir, i), bbox_inches='tight')

                # Node is leaf node
                if str(i) in self.leafs:
                    p = list(modules[i].classifier.parameters())[1]#.fc.parameters())
                    m = nn.Softmax()
                    p = m(p).data.numpy()
                    self.plot_actions(p, str(i))
                    self.distributions[i] = p
                    node = self.tree.search_nodes(name=str(i))[0]
                    self.backtrack_and_calc_classpath(node)


        # SDT
        elif self.type == "SDT":
            modules = self.model.weights
            self.distributions = [[]] * len(modules)
            for i in range(len(modules)):
                w = modules[i]
                w = w.detach().numpy()
                w = w.reshape(width, height)
                plt.clf()
                plt.imshow(w, cmap='gray')
                # plt.colorbar()
                plt.xticks([])
                plt.yticks([])
                # plt.show()
                plt.savefig("{}{}.svg".format(wdir, i), bbox_inches='tight')

                # Node is leaf node
                if str(i) in self.leafs:
                    p = self.model.leafs[i]  # .fc.parameters())
                    m = nn.Softmax()
                    p = m(p).data.numpy()
                    self.plot_actions(p, str(i))
                    self.distributions[i] = p
                    node = self.tree.search_nodes(name=str(i))[0]
                    self.backtrack_and_calc_classpath(node)

        self.add_classpaths()

    # Add visualised images to nodes in tree
    def add_node_visuals(self):
        wdir = './.working/'
        nodes = self.tree.search_nodes()[1:]
        for i in range(len(nodes)):
            node = nodes[i]
            path = "{}{}.svg".format(wdir, i)
            face = ImgFace(path)
            face.rotation = -90
            node.add_face(face, column=1)
            # Add extra plot under leaf
            if str(i) in self.leafs:
                child_name = '{}_dist'.format(str(i))
                node.add_child(name=child_name)
                child_node = self.tree.search_nodes(name=child_name)[0]
                path = "{}{}_dist.png".format(wdir, i)
                face = ImgFace(path)
                face.rotation = -90
                child_node.add_face(face, column=1)

    # Draw path on tree
    def draw_path(self, path):
        self.clear_path()
        for node_name in path:
            node = self.tree.search_nodes(name=str(node_name))[0]
            node.img_style['hz_line_color'] = 'green'
            node.img_style['hz_line_width'] = 20
            node.img_style['vt_line_color'] = 'green'
            node.img_style['vt_line_width'] = 20
            node.img_style['fgcolor'] = 'green'
            node.img_style['size'] = 50

    # Remove path from tree
    def clear_path(self):
        for node in self.tree.search_nodes():
            node.img_style['hz_line_color'] = 'black'
            node.img_style['hz_line_width'] = 0
            node.img_style['vt_line_color'] = 'black'
            node.img_style['vt_line_width'] = 0
            node.img_style['fgcolor'] = 'black'
            node.img_style['size'] = 0

    # Generate action probability chart
    def plot_actions(self, y, name):
        plt.clf()
        wdir = '.working/'
        x = range(0, len(y))
        plt.ylim(min(y) - 0.005 * min(y), max(y) + 0.005 * max(y))
        plt.xlabel('Action')
        plt.ylabel('Probability')
        plt.xticks(range(0, len(y)))
        plt.bar(x, y)
        plt.savefig("{}{}_dist.png".format(wdir, name), dpi=65)

    # Backtrack from every leaf to root for classes indication
    def backtrack_and_calc_classpath(self, leaf):
        class_path = [leaf]
        parent = leaf.up
        class_path.append(parent)

        while not str(parent.name) in ['0']:
            parent = parent.up
            class_path.append(parent)
        self.class_paths.append(class_path)
        self.path_starts.append(leaf)

    # Add classes indication to nodes
    def add_classpaths(self):
        n_nodes = len(list(self.tree.search_nodes()))
        result = [""] * n_nodes
        for class_path in self.class_paths:
            class_leaf = class_path[0]
            best_action = np.argmax(self.distributions[int(class_leaf.name)])
            # First leaf
            result[int(class_leaf.name)] = result[int(class_leaf.name)] + " " + str(best_action)
            # All other leafs
            parent = class_leaf.up
            while not str(parent.name) == '0':
                parent = parent.up
                result[int(parent.name)] = result[int(parent.name)] + " " + str(best_action)
            # Root case
            parent = class_leaf.up
            result[int(parent.name)] = result[int(parent.name)] + " " + str(best_action)

        # Add class names
        for node in list(self.tree.search_nodes()):
            if not node.name == '':
                indx = int(node.name)
                classes = result[indx]
                classes = list(set(classes.split(" ")))
                classes.sort()
                classes.remove('')
                classes = ' '.join(classes)

                # Add text face
                F = TextFace(classes, tight_text=True, fsize=30)
                F.rotation = -90
                node.add_face(F, column=0, position="branch-right")
















