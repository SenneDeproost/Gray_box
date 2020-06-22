from ete3 import Tree, TreeStyle, NodeStyle
t = Tree()
t.populate(10)
ts = TreeStyle()
ts.show_leaf_name = True
ts.rotation = 90
ns = NodeStyle()
ns.
t.show(tree_style=ts)