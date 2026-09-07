"""Pipeline configuration for the OPS-SAT-AD anomaly-detection example.

Python analogue of FogML-C's src/fogml_config.h
(https://github.com/tszydlo/FogML-C): the reservoir-sampling + LOF
config lives here as SatPipelineConfig/SatPipeline, with
fogml_learning()/fogml_processing() as the two entry points main.py
drives per CSV row — same shape as the C file's global config structs
plus its fogml_learning()/fogml_processing() functions.
"""

from dataclasses import dataclass
from typing import Optional

from fogml_sdk.anomaly_rt import (
    TinymlLof,
    TinymlLofConfig,
    TinymlReservoirSampling,
    TinymlReservoirSamplingConfig,
)


@dataclass
class SatPipelineConfig:
    vector_size: int = 16  # FOGML_VECTOR_SIZE — number of DSP feature columns per row
    reservoir_size: int = 30  # MY_RESERVOIR_SIZE
    lof_k: int = 4  # parameter_k — k nearest neighbours considered by LOF
    anomaly_threshold: float = 1.5  # score > threshold -> classified anomalous -> can be modified

class SatPipeline:
    """Replica of fogml_config.h's global config + fogml_learning/fogml_processing."""

    def __init__(self, config: Optional[SatPipelineConfig] = None):
        self.config = config or SatPipelineConfig()
        self.reservoir = TinymlReservoirSamplingConfig(
            n=self.config.reservoir_size, vector_size=self.config.vector_size
        )
        self.lof = TinymlLofConfig(parameter_k=self.config.lof_k, data=self.reservoir.reservoir)
        TinymlLof.tinyml_lof_init(self.lof)

    def fogml_learning(self, vector) -> None:
        TinymlReservoirSampling.tinyml_reservoir_sampling(vector, self.reservoir)

        # LOF should only consider the filled part of the reservoir until it's full
        self.lof.n = min(self.reservoir.k, self.config.reservoir_size)

        TinymlLof.tinyml_lof_learn(self.lof)

    def fogml_processing(self, vector) -> float:
        print(TinymlReservoirSampling.info(self.reservoir))

        try:
            # LOF should only consider the filled part of the reservoir until it's full
            self.lof.n = min(self.reservoir.k, self.config.reservoir_size)

            score = TinymlLof.tinyml_lof_score(vector, self.lof)
        except RuntimeError:
            score = 0.0

        return score
