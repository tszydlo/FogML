"""Replica of fogml_sdk/ports/fogml_ports.h.

The C SDK has three port backends (POSIX, Arduino, Zephyr) selected at
compile time, all exposing the same contract:

    fogml_random(min, max)   -> uniform random int in [min, max)
    fogml_printf(str)
    fogml_printf_float(number)
    fogml_printf_int(number)

Python has a single runtime, so there is one implementation here rather
than a set of conditionally-compiled backends.
"""

import random

_rng = random.Random()


def set_seed(seed) -> None:
    """Seed the module-level RNG, for reproducible runs of RNG-driven modules."""
    _rng.seed(seed)


def fogml_random(min: int, max: int) -> int:
    """Uniform random int in [min, max), matching all three C ports:

    POSIX:   min + rand() % (max - min)
    Arduino: random(min, max)
    Zephyr:  sys_rand32_get() % (max - min) + min
    """
    return _rng.randrange(min, max)


def fogml_printf(text: str) -> None:
    print(text, end="")


def fogml_printf_float(number: float) -> None:
    print(f"{number:.6f}", end="")


def fogml_printf_int(number: int) -> None:
    print(int(number), end="")
