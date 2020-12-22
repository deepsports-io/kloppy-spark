from __future__ import annotations

from typing import Tuple

from pyspark import SparkContext
from pyspark.sql import SparkSession

from .utils.graph import Graph


class Pipeline:
    def __init__(self, name: str, sc: SparkContext) -> None:
        self.name = name
        self.dag = Graph()
        self.sc = sc
        self.spark = SparkSession(self.sc)

    def add_source(self, name: str, source: "Source") -> Pipeline:
        self.dag.add_vertex(name, source)
        return self

    def add_stage(self, pre_stage: str, name: str, stage: "Stage") -> Pipeline:
        self.dag.add_vertex(name, stage)
        self.dag.add_edge(pre_stage, name)
        return self

    def __and__(self, args: Tuple[str, "Source"]) -> Pipeline:
        return self.add_source(*args)

    def __or__(self, args: Tuple[str, str, "Stage"]) -> Pipeline:
        return self.add_stage(*args)

    def add_sink(self, pre_stage: str, name: str, sink: "Sink") -> Pipeline:
        self.dag.add_vertex(name, sink)
        self.dag.add_edge(pre_stage, name)
        return self

    def run(self):
        inputs = {}
        for stage_input, key, stage in self.dag.topological_sort():
            stage_input = inputs[stage_input] if stage_input else None
            inputs[key] = stage.process(pipeline=self, inputs=stage_input)
