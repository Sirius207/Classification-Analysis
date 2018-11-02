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





# TODO: class RuleGenerator

# TODO: class dataGenerator