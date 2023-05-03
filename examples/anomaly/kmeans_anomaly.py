from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

from src.fogml.anomaly import KMeansAnomalyDetector
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

    return (spX, spY)

(spX, _) = fogml_prepare_data(DATA)
(spX_test, y) = fogml_prepare_data(DATA_TEST)

print(y)

scaler = MinMaxScaler()
transformer = scaler.fit(spX)
data_norm = transformer.transform(spX)

print("Scaler:")
print(scaler.data_min_)
print(scaler.data_max_)

anomalyDetector = KMeansAnomalyDetector(n_clusters=16)
anomalyDetector.fit(data_norm)

data_test_norm = transformer.transform(spX_test)
res = anomalyDetector.predict(data_test_norm)
print(res)

factory = GeneratorFactory()
generator = factory.get_generator(transformer)
generator.generate()

generator = factory.get_generator(anomalyDetector)
generator.generate()
