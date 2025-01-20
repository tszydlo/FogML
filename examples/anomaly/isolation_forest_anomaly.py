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

##################################################################
anomalyDetector = IsolationForestAnomalyDetector(n_estimators=100, max_samples='auto', random_state=42)
anomalyDetector.fit(spX)
##################################################################

res = anomalyDetector.predict(spX_test)

factory = GeneratorFactory()
generator = factory.get_generator(anomalyDetector)
generator.generate()