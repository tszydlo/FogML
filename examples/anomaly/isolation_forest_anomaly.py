from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

from src.fogml.anomaly import IsolationForestAnomalyDetector
from src.fogml.generators import GeneratorFactory

DATA = ["0_idle.csv", "1_circle.csv", "2_snake.csv"]
DATA_TEST = ["0_idle.csv", "1_circle.csv", "2_snake.csv", "3_up_down.csv"]


def fogml_prepare_data(data):
    spX_t = []
    spY_t = []

    i = 0
    for fname in data:
        tmp = pd.read_csv(fname, delimiter=" ", header=None)
        spX_t.append(tmp)
        spY_t.append([i] * tmp.shape[0])
        i = i + 1

    spX = np.concatenate(spX_t, axis=0)
    spY = np.concatenate(spY_t, axis=0)

    return spX, spY


(spX, _) = fogml_prepare_data(DATA)
(spX_test, y) = fogml_prepare_data(DATA_TEST)

print(y)

scaler = MinMaxScaler()
transformer = scaler.fit(spX)
data_norm = transformer.transform(spX)

data_test_norm = transformer.transform(spX_test)

print("Scaler:")
print(scaler.data_min_)
print(scaler.data_max_)

##################################################################
anomalyDetector = IsolationForestAnomalyDetector(n_estimators=100, max_samples='auto', random_state=42)
anomalyDetector.fit(data_norm)
##################################################################

# TODO: the results of predict are not correct? maybe use threshold?
res = anomalyDetector.predict(data_test_norm)
print(res)

factory = GeneratorFactory()
generator = factory.get_generator(transformer)
generator.generate()

generator = factory.get_generator(anomalyDetector)
generator.generate()
