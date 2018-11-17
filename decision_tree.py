import logging
import pandas as pd
from sklearn import tree
from sklearn.metrics import accuracy_score

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


# Constants
training_propotion_list = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

data = pd.read_csv('data/training.csv')


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
    testing_x = data.values[training_data_size:,0:x_column_size]
    predict_y = clf.predict(testing_x)
    test_y = data['y'][training_data_size:]

    acc = accuracy_score(test_y,predict_y)*100

    logger.info(f'Training Percent: {training_propotion}, Acc: {acc}')
    return acc


def iterate_each_training_propotion(data):
    for propotion in training_propotion_list:
        calculate_acc(data, propotion)

iterate_each_training_propotion(data)
