import pandas as pd
from sklearn import tree
from sklearn.metrics import accuracy_score

training_data_propotion = 0.8

# get data
data = pd.read_csv('training.csv')
training_data_size = int(training_data_propotion * len(data))
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

print(acc)
