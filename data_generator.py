import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


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

def write_rules_file(rules, file_path):
    with open(file_path + 'rules.json', 'w') as output:
        output.write(str(rules))

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
    for data_id in range(options['data_len']):
        new_data = ''
        # create feature values
        column_size = options['real_columns'] + options['fake_columns']
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

    logger.info(f'Real_columns: {options["real_columns"]}')
    logger.info(f'Fake_columns: {options["fake_columns"]}')
    logger.info(f'Choices: {options["choices"]}')
    logger.info(f'Data Length: {options["data_len"]}')
    return data_list

def write_data_file(data_list, file_path):
    head = ''
    x_column_size = len(data_list[0].split(',')) - 1
    for id in range(x_column_size):
        new_value = 'F' + str(id)
        if (len(head) == 0):
            head += new_value
        else:
            head += ',' + new_value
    head += ',' + 'y'

    with open(file_path + 'training.csv', 'w') as output:
        output.write(head + '\n')
        for data in data_list:
            output.write(data + '\n')

#
# Check Data Condition
#

def check_population_percent(data_list, options):
    # calculate population number
    population = {}
    percent_trend = {}
    five_percent_data_len = int(len(data_list)/20)
    real_population_len = options['choices']**(options['real_columns'])

    for id, data in enumerate(data_list):
        feature_end_index = options['real_columns'] * 2 - 1
        feature_value = data[0:feature_end_index]
        if feature_value not in population:
            population[feature_value] = 1
        else:
            population[feature_value] + 1

        # calculate percent of population per 10% data
        if id % five_percent_data_len == 0 and id > 1:
            current_percent = len(population)/real_population_len
            current_index = int(id / five_percent_data_len) * 5
            percent_trend[current_index] = current_percent

    data_population_len = len(population)
    population_percent = data_population_len/real_population_len

    logger.info(f'Data_population_trend: {percent_trend}')
    logger.info(f'Data_population_len: {data_population_len}')
    logger.info(f'Real_population_len: {real_population_len}')
    logger.info(f'Population_percent: {population_percent}')
    logger.info(f'Data length: {options["data_len"]}')

    return percent_trend

def write_trend_file(trend, file_path):
    with open(file_path + 'trend.json', 'w') as output:
        output.write(str(trend))

#
# Part 3: Main Function
#

def main (options):
    file_path = 'data/r{}_f{}_c{}/'.format(options['real_columns'], options["fake_columns"], options['choices'])

    # rules generation
    root = generate_random_tree(options['real_columns'] + 1, options['choices'], True)
    rules = tree_to_list(root)
    write_rules_file(rules, file_path)

    # data generation
    data_list = get_random_data(options, rules)
    percent_trend = check_population_percent(data_list, options)

    write_trend_file(percent_trend, file_path)
    write_data_file(data_list, file_path)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--real_columns',
                       default=3,
                       help='input real column number')
    parser.add_argument('--fake_columns',
                        default=3,
                        help='input fake column number')
    parser.add_argument('--choices',
                       default=5,
                       help='input column max choices')
    parser.add_argument('--data_len',
                       default=2000,
                       help='input length of data')
    args = parser.parse_args()

    options = {
        'real_columns': int(args.real_columns),
        'fake_columns': int(args.fake_columns),
        'choices': int(args.choices),
        'data_len': int(args.data_len),
    }

    main(options)