import logging
import pandas as pd
from sklearn import tree
from sklearn.metrics import accuracy_score

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


# Constants
data_config = [
    'r3_f3_c5',
    'r3_f6_c5',
    'r3_f9_c5',
    'r3_f12_c5',
    'r3_f15_c5'
]
training_propotion_list = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9]
testing_propotion = 0.1

fit_index = '50'
basic_path = 'data/{}/'.format(fit_index)


def calculate_acc(data, training_propotion):
    # split training data
    training_data_size = int(training_propotion * len(data))
    x_column_size = len(data.iloc[0]) - 1

    training_x = data.values[0:training_data_size,0:x_column_size]
    training_y = data['y'][0:training_data_size]

    # training
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(training_x, training_y)

    # testing
    testing_data_size = int((1 - testing_propotion) * len(data))
    testing_x = data.values[testing_data_size:,0:x_column_size]
    test_y = data['y'][testing_data_size:]

    predict_y = clf.predict(testing_x)
    acc = accuracy_score(test_y,predict_y)*100
    logger.info(f'Training Percent: {training_propotion}, Acc: {acc}')

    # graph
    max_depth = clf.tree_.__getstate__()['max_depth']
    node_count = clf.tree_.__getstate__()['node_count']
    logger.info(f'Max depth: {max_depth}')
    logger.info(f'Node count: {node_count}')

    return (acc, max_depth, node_count)


def iterate_each_training_propotion(data):
    acc_list = []
    depth_list = []
    node_count_list = []
    for propotion in training_propotion_list:
        results = calculate_acc(data, propotion)
        acc_list.append(results[0])
        depth_list.append(results[1])
        node_count_list.append(results[2])
    return (acc_list, depth_list, node_count_list)


def iterate_each_training_data(data_config):
    def generate_transaction_list(data_path, single_results_list):
        return data_path + ',' + ','.join(str(acc) for acc in single_results_list)

    acc_transaction_list = []
    depth_transaction_list = []
    node_transaction_list = []

    for data_path in data_config:
        logger.info(f'Training Data: {data_path} ----------------')
        data = pd.read_csv(basic_path + data_path + '/training.csv')
        results_list = iterate_each_training_propotion(data)

        acc_transcation = generate_transaction_list(data_path, results_list[0])
        acc_transaction_list.append(acc_transcation)

        depth_transcation = generate_transaction_list(data_path, results_list[1])
        depth_transaction_list.append(depth_transcation)

        node_transcation = generate_transaction_list(data_path, results_list[2])
        node_transaction_list.append(node_transcation)


    return (acc_transaction_list, depth_transaction_list, node_transaction_list)


def write_results(transaction_list):
    def write_data(output, head, transaction_list):
        output.write(head)

        for transaction in transaction_list:
            output.write(transaction + '\n')

    with open(basic_path + 'acc.csv', 'w') as acc_output, \
        open(basic_path + 'depth.csv', 'w') as depth_output, \
        open(basic_path + 'node.csv', 'w') as node_output:

        head = 'type,' + ','.join(str(p) for p in training_propotion_list) + '\n'

        write_data(acc_output, head, transaction_list[0])
        write_data(depth_output, head, transaction_list[1])
        write_data(node_output, head, transaction_list[2])


transaction_list = iterate_each_training_data(data_config)
write_results(transaction_list)