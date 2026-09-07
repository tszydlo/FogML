"""Replica of fogml_sdk/anomaly_rt/fogml_reservoir.{h,c}.

Note this is *not* classic (Vitter) reservoir sampling: the C
implementation never tracks the total number of items seen. Once the
reservoir is full, every subsequent sample overwrites a uniformly
random slot in [0, n) — a random-replacement policy, not one weighted
by stream length. That behavior is intentionally preserved here rather
than "corrected".
"""

from dataclasses import dataclass, field

import numpy as np

from fogml_sdk import ports


@dataclass
class TinymlReservoirSamplingConfig:
    """Replica of tinyml_reservoir_sampling_config_t."""

    n: int  # size of reservoir
    vector_size: int  # number of elements in the vector
    k: int = 0  # number of elements currently in reservoir
    reservoir: np.ndarray = field(init=False)  # shape (n, vector_size)

    def __post_init__(self) -> None:
        self.reservoir = np.zeros((self.n, self.vector_size), dtype=np.float32)

    def reset(self) -> None:
        """Empty the reservoir: zero the collected-point count and clear the buffer."""
        self.k = 0
        self.reservoir[:] = 0


class TinymlReservoirSampling:
    """Replica of fogml_sdk's tinyml_reservoir_sampling(), namespaced as a static method."""

    @staticmethod
    def tinyml_reservoir_sampling(vector, config: TinymlReservoirSamplingConfig) -> None:
        """Replica of tinyml_reservoir_sampling(float *vector, ...)."""
        vector = np.asarray(vector, dtype=np.float32)

        if config.k < config.n:
            config.reservoir[config.k] = vector
            config.k += 1
        else:
            i = ports.fogml_random(0, config.n)
            if i < config.n:  # always true in C too; kept for fidelity to the source
                config.reservoir[i] = vector

    @staticmethod
    def info(config: TinymlReservoirSamplingConfig) -> str:
        """Return a pandas/numpy-.info()-style summary of the reservoir buffer."""
        fill_pct = 100.0 * config.k / config.n if config.n else 0.0
        return (
            "TinymlReservoirSampling buffer\n"
            f"  capacity (n):   {config.n}\n"
            f"  filled (k):     {config.k} ({fill_pct:.1f}%)\n"
            f"  is_full:        {config.k >= config.n}\n"
            f"  vector_size:    {config.vector_size}\n"
            f"  shape:          {config.reservoir.shape}\n"
            f"  dtype:          {config.reservoir.dtype}\n"
            f"  memory usage:   {config.reservoir.nbytes} bytes"
        )
