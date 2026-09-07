"""fogml_sdk — Python replica of the FogML SDK (https://github.com/tszydlo/fogml_sdk).

Mirrors the SDK's module layout (see fogml_sdk/fogml.h) so that
trained/generated models can be exercised from Python with the same
runtime semantics the C SDK gives an on-device build, without needing
a C toolchain:

    ports        fogml_sdk/ports/fogml_ports.h
    anomaly      fogml_sdk/anomaly/fogml_anomaly.{h,c}          (not yet implemented)
    anomaly_rt   fogml_sdk/anomaly_rt/fogml_reservoir.{h,c}, fogml_lof.{h,c} (lof backed by scikit-learn)
    classifier   fogml_sdk/classifier/fogml_classifier.h        (not yet implemented)
    scaler       fogml_sdk/scaler/fogml_scaler.{h,c}            (not yet implemented)
    dsp          fogml_sdk/dsp/fogml_dsp.{h,c}                  (not yet implemented)
    rl           fogml_sdk/rl/fogml_rl.h                        (not yet implemented)

Only submodules with a working implementation are imported here;
stub modules raise NotImplementedError on import and are reached via
their explicit submodule path, e.g. `fogml_sdk.anomaly.detector`.
"""

from fogml_sdk.anomaly_rt import (
    TinymlLof,
    TinymlLofConfig,
    TinymlReservoirSampling,
    TinymlReservoirSamplingConfig,
)

__all__ = [
    "TinymlReservoirSamplingConfig",
    "TinymlReservoirSampling",
    "TinymlLofConfig",
    "TinymlLof",
]
