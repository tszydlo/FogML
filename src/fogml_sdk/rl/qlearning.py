"""Replica of fogml_sdk/rl/fogml_rl.h — inference-side Q-learning.

Not yet implemented. C API to mirror (implementation is generated per
project from src/fogml/generators/skeletons/qlearning_model_skeleton.txt,
not shipped by the SDK itself):

    fogml_qlearning_init()
    fogml_qlearning_update_state(state)
    fogml_qlearning_select_action() -> int
    FOGML_RL_STATES / FOGML_RL_ACTIONS / FOGML_RL_OBSERVATION_SIZE

Distinct from src/fogml/rl/qlearning.py, which is the *training*-side
Q-table/discretizer builder used by the code generators — this module
is the *inference*-side runtime replica of the generated device code.
"""

raise NotImplementedError("fogml_sdk.rl.qlearning is not implemented yet")
