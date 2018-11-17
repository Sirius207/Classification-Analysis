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
training_propotion_list = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
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
    return acc


def iterate_each_training_propotion(data):
    acc_list = []
    for propotion in training_propotion_list:
        acc_list.append(calculate_acc(data, propotion))
    return acc_list


def iterate_each_training_data(data_config):
    transaction_list = []
    for data_path in data_config:
        logger.info(f'Training Data: {data_path} ----------------')
        data = pd.read_csv(basic_path + data_path + '/training.csv')
        acc_list = iterate_each_training_propotion(data)
        transcation = data_path + ',' + ','.join(str(acc) for acc in acc_list)
        transaction_list.append(transcation)
    return transaction_list


def write_acc_results(transaction_list):
    with open(basic_path + 'results.csv', 'w') as output:
        head = 'type,' + ','.join(str(p) for p in training_propotion_list) + '\n'
        output.write(head)

        for transaction in transaction_list:
            output.write(transaction + '\n')


transaction_list = iterate_each_training_data(data_config)
write_acc_results(transaction_list)