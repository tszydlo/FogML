"""Replica of fogml_sdk/classifier/fogml_classifier.h.

Not yet implemented. C API to mirror:

    int classifier(float *x)

Unlike the other SDK modules, this header declares an interface that
generated model code implements (fogml's Bayes/tree/MLP/random-forest
generators each emit a `classifier`-shaped function) — the SDK itself
provides no default implementation. The Python equivalent should be a
Protocol (Callable[[Sequence[float]], int]) that generated-model
replicas can be checked against, not a concrete implementation.
"""

raise NotImplementedError("fogml_sdk.classifier is not implemented yet")
