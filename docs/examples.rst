:parenttoc: True

Examples
========

Arduino Digit Recognition
-------------------------


.. figure:: ./images/arduino_tft.png
  :width: 600

Zephyr OS
---------

The application recognizes gestures an IoT device performs based on the built-in accelerometer. It uses the
classification algorithms and programming tools provided by FogML:

* FogML-SDK [https://github.com/tszydlo/fogml_sdk]
* FogML tools [https://github.com/tszydlo/FogML]

The application is implemented for the Zephyr-OS operating system. The tests were carried out on a ``Thingy:91``
device containing nrf9160 and manufactured by Nordic Semiconductor.

**Classification**

The accelerometer data processing pipeline is presented in the figure.

.. figure:: ./images/examples_zephyr_classification.png
  :width: 600

**Classification pipeline**

In the example, gestures are classified using the random forest algorithm. The generated classifier source code is in
the ``src/fogml_generated/random_forest_model.c`` file.

For the device to recognize other gestures, it is necessary to collect training data, assign labels, and train the
model. The entire process is described in Jupyter Notebook, along with training data in the tools directory. Notepad
can be run in eg Google Colab or Anaconda.

**Anomaly detection**

The example uses the modification of the K-Means algorithm and z-score to detect anomalies - deviations from training
data. Model generation for this purpose is described in Jupyter Notebook located in the tools directory.
Building

The application is implemented for the Zephyr OS operating system. Since the application is for ``Thingy:91`` device,
we use NRF Connect SDK 2.0.0 and VSCode plugin, which simplifies the process of building, flashing and debugging
applications for Zephyr. The application can also be built directly using the west tool and the base Zephyr.

The application uses the basic drivers available in the operating system, and porting to another device should be
relatively easy.

Complex examples
----------------

**Satellite telemetry**

This example implements an online, semi-supervised anomaly detector for the `OPS-SAT-AD` [https://github.com/kplabs-pl/OPS-SAT-AD] satellite telemetry benchmark, using reservoir sampling and Local Outlier Factor (LOF) from the FogML SDK's ``anomaly_rt`` module. A model is built incrementally from the non-anomalous rows of a telemetry channel's training split, then used to score the remaining rows, classifying a row as anomalous when its LOF score exceeds a threshold. See the paper [https://arxiv.org/abs/2206.14265] for the underlying algorithm.

The C version, `FogML-C` [https://github.com/tszydlo/FogML-C], is a plain, host-buildable example (``Makefile`` + ``gcc``, no board framework) that links directly against the vendored ``fogml_sdk`` C library. Its pipeline configuration - reservoir size, LOF ``k``, feature-vector size - lives in ``src/fogml_config.h``, and ``src/main.c`` drives it over a per-channel CSV, printing per-row scores and a final accuracy summary.

The Python port lives in this repository's ``examples/sat``. It mirrors the same structure and CSV-driven CLI, using ``fogml_sdk``'s Python replica of ``anomaly_rt`` (reservoir sampling, and LOF backed by scikit-learn) in place of the compiled C SDK, with the pipeline configuration in ``fogml_config.py`` and the driver in ``main.py`` - no C toolchain required.

