import random

class Tree:
    def __init__(self, feature):
        self.feature = feature
        self.children = None

    def insert_node(self, feature):
        new_node = Tree(feature)
        if self.children == None:
            self.children = []
            self.children.append(new_node)
        else:
            self.children.append(new_node)

        return self.children[-1]

#
# Part 1: Rules Generation
#

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
                    new_child = current_node.insert_node('L'+str(current_level))
                    grow(new_child, current_level+1, final_level, max_degree)
        else:
            current_node.feature = 'A' if random.randint(0, 1) == 0 else 'B'

    root = Tree('L0')
    grow(root, 1, level, max_degree)
    return root


def tree_to_list(tree):
    def traversal(node, tree_list):
        if node.children != None:
            for id, value in enumerate(node.children):
                if node.children[id].children != None:
                    tree_list.append([])
                    sub_dict = tree_list[-1]
                    sub_node = node.children[id]
                    traversal(sub_node, sub_dict)
                else:
                    tree_list.append(node.children[id].feature)
        else:
            tree_list = node.feature

    tree_list = []
    traversal(tree, tree_list)
    return tree_list


#
# Part 2: Data Generation
#


def get_label(data, rules):
    features = data.split(',')
    sub_choice = rules
    for feature in features:
        if isinstance(sub_choice, list):
            sub_choice = sub_choice[int(feature)]
        else:
            break

    return sub_choice

def get_random_data(options, rules):
    data_list = []
    for data_id in range(options['data_length']):
        new_data = ''
        # create feature values
        column_size = options['x_columns'] + options['fake_columns']
        for column_id in range(column_size):
            new_value = str(random.randint(0, options['choices']-1))
            if (len(new_data) == 0):
                new_data += new_value
            else:
                new_data +=  ',' + new_value

        # add y value
        if (rules):
            label = get_label(new_data, rules)
            new_data +=  ',' + label

        data_list.append(new_data)
    return data_list

def write_data_file(data_list):
    head = ''
    x_column_size = len(data_list[0].split(',')) - 1
    for id in range(x_column_size):
        new_value = 'F' + str(id)
        if (len(head) == 0):
            head += new_value
        else:
            head += ',' + new_value
    head += ',' + 'y'

    with open('training.csv', 'w') as output:
        output.write(head + '\n')
        for data in data_list:
            output.write(data + '\n')

#
# Part 3: Main
#

options = {
    'x_columns': 2,
    'choices': 2,
    'data_length': 50,
    'fake_columns': 3
}

root = generate_random_tree(options['x_columns'] + 1, options['choices'], True)
rules = tree_to_list(root)

print(rules)

data = get_random_data(options, rules)
write_data_file(data)