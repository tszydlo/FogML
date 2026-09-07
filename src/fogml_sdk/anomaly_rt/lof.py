"""Replica of fogml_sdk/anomaly_rt/fogml_lof.{h,c} — Local Outlier Factor.

The C SDK computes k-distance/lrd/score with a brute-force O(n) neighbour
search over `data`. This replica keeps the same config/init/learn/score
calling convention but delegates the actual neighbour search and LOF math
to scikit-learn's LocalOutlierFactor (novelty mode).
"""

from dataclasses import dataclass, field

import numpy as np
from sklearn.neighbors import LocalOutlierFactor


@dataclass
class TinymlLofConfig:
    """Replica of tinyml_lof_config_t."""

    parameter_k: int  # k nearest neighbours are considered
    data: np.ndarray  # set of points, shape (capacity, vector_size)
    n: int = field(init=False)  # number of *valid* points in data — may be < data.shape[0]
                                 # (e.g. a fixed-capacity buffer that's still filling up); callers
                                 # may lower it after construction, same as the C struct's `n`
                                 # being independent of the `data` pointer's allocated size
    vector_size: int = field(init=False)  # dimension of each point
    k_distance: np.ndarray = field(init=False)  # (n,) k-distance for each point
    lrd: np.ndarray = field(init=False)  # (n,) local reachability density for each point
    _estimator: LocalOutlierFactor = field(init=False, default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.data = np.asarray(self.data, dtype=np.float32)
        self.n, self.vector_size = self.data.shape
        self.k_distance = np.zeros(self.n, dtype=np.float32)
        self.lrd = np.zeros(self.n, dtype=np.float32)


class TinymlLof:
    """Replica of fogml_sdk's tinyml_lof_* functions, namespaced as static methods."""

    @staticmethod
    def tinyml_lof_init(config: TinymlLofConfig) -> None:
        """Replica of tinyml_lof_init — a no-op in the SDK too."""

    @staticmethod
    def tinyml_lof_learn(config: TinymlLofConfig) -> None:
        """Replica of tinyml_lof_learn.

        Fits a scikit-learn LOF model on config.data[:config.n] (not the whole
        buffer — see the TinymlLofConfig.n docstring) and mirrors its per-point
        k-distance/lrd back onto the config for parity with the C struct; the
        fitted estimator itself is kept for tinyml_lof_score.
        """
        if config.n < config.parameter_k + 1:
            return

        estimator = LocalOutlierFactor(n_neighbors=config.parameter_k, novelty=True, metric="euclidean")
        estimator.fit(config.data[: config.n])

        config._estimator = estimator
        config.k_distance = estimator._distances_fit_X_[:, -1].astype(np.float32)
        config.lrd = estimator._lrd.astype(np.float32)

    @staticmethod
    def tinyml_lof_score(vector, config: TinymlLofConfig) -> float:
        """Replica of tinyml_lof_score."""
        if config.n < config.parameter_k + 1:
            return 0.0
        if config._estimator is None:
            raise RuntimeError("tinyml_lof_learn(config) must be called before tinyml_lof_score()")

        vector = np.asarray(vector, dtype=np.float32).reshape(1, -1)
        return float(-config._estimator.score_samples(vector)[0])
