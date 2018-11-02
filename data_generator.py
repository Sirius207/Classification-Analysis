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


def generate_binary_tree(level):
    def grow(current_node, current_level, final_level):
        if final_level != current_level:
            left_child = current_node.insert_node('left', current_level)
            right_child = current_node.insert_node('right', current_level)
            grow(left_child, current_level+1, final_level)
            grow(right_child, current_level+1, final_level)

    root = Tree(1)
    grow(root, 1, level)
    return root


# TODO: class RuleGenerator

# TODO: class DataGenerator
