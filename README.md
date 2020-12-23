# kloppy-spark
Spark Helpers for Kloppy

[![PyPI Latest Release](https://img.shields.io/pypi/v/kloppy-spark.svg)](https://pypi.org/project/kloppy-spark/)
[![Downloads](https://pepy.tech/badge/kloppy-spark/month)](https://pepy.tech/project/kloppy-spark/month)
![](https://img.shields.io/github/license/deepsports-io/kloppy-spark)
[![Powered by Deepsports](https://img.shields.io/badge/Powered%20by-Deepsports-888888)](https://deepsports.io)

## Running the example notebook

### Requirements

* Apache Spark 3.0.1
* Jupyter Lab

### Starting Jupyter Lab in Apache Spark

```bash
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS=lab

pyspark --packages graphframes:graphframes:0.8.1-spark3.0-s_2.12
```

A browser window should open, and you can open and run the example notebook.