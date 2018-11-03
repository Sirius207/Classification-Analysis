import random

class Tree:
    def __init__(self, feature):
        self.feature = feature
        self.children = None

    def insert_node(self, value, feature):
        if self.children == None:
            self.children = {}
            self.children[value] = Tree(feature)
        else:
            self.children[value] = Tree(feature)

        return self.children[value]


def generate_random_tree(level, max_degree, is_full_degree=False):
    def grow(current_node, current_level, final_level, max_degree):
        if final_level != current_level:


            if is_full_degree:
                current_node_degree = max_degree
            else:
                current_node_degree = random.randint(0, max_degree)

            if current_node_degree == 0:
                current_node.feature = 'A' if random.randint(0, 1) == 0 else 'B'
            else:
                for number in range(current_node_degree):
                    new_child = current_node.insert_node('C'+str(number), 'L'+str(current_level))
                    grow(new_child, current_level+1, final_level, max_degree)
        else:
            current_node.feature = 'A' if random.randint(0, 1) == 0 else 'B'

    root = Tree('L0')
    grow(root, 1, level, max_degree)
    return root


def tree_to_dict(tree):
    def traversal(node, tree_dict):
        if node.children != None:
            tree_dict[node.feature] = {}
            for value in node.children:
                if node.children[value].children != None:
                    tree_dict[node.feature][value] = {}
                    sub_dict = tree_dict[node.feature][value]
                    sub_node = node.children[value]
                    traversal(sub_node, sub_dict)
                else:
                    tree_dict[node.feature][value] = node.children[value].feature
        else:
            tree_dict = node.feature

    tree_dict = {}
    traversal(tree, tree_dict)
    return tree_dict




# TODO: class DataGenerator
