from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Dict, Tuple, TypeVar

from pyspark import SparkContext
from pyspark.sql import SparkSession

from .utils.graph import Graph

Stage = TypeVar("Stage")
Source = TypeVar("Source")
Sink = TypeVar("Sink")


@dataclass
class Vertex:
    name: str
    stage: Stage
    inputs: Dict[str, str]


class Pipeline:
    def __init__(self, name: str, sc: SparkContext) -> None:
        self.name = name
        self.dag = Graph()
        self.sc = sc
        self.spark = SparkSession(self.sc)
        self.intermediate_results = {}

    def add_source(self, name: str, source: Source) -> Pipeline:
        vertex = Vertex(name=name, stage=source, inputs=None)
        self.dag.add_vertex(name, vertex)
        return self

    def add_stage(self, name: str, stage: Stage, **kwargs: Dict[str, str]) -> Pipeline:
        vertex = Vertex(name=name, stage=stage, inputs=kwargs)
        self.dag.add_vertex(name, vertex)
        for pre_stage in kwargs.values():
            self.dag.add_edge(pre_stage, name)
        return self

    def __and__(self, args: Tuple[str, Source]) -> Pipeline:
        return self.add_source(*args)

    def __or__(self, args: Tuple[str, Stage, Dict[str, str]]) -> Pipeline:
        return self.add_stage(args[0], args[1], **args[2])

    def add_sink(self, name: str, sink: "Sink", **kwargs: Dict[str, str]) -> Pipeline:
        return self.add_stage(name, sink, **kwargs)

    def run(self):
        self.intermediate_results = {}
        for _, _, vertex in self.dag.topological_sort():
            stage_inputs = dict(
                [
                    (key, self.intermediate_results[stage_input])
                    for key, stage_input in (vertex.inputs or {}).items()
                ]
            )
            self.intermediate_results[vertex.name] = vertex.stage.process(
                pipeline=self, **stage_inputs
            )

    def _validate(self, stage) -> bool:
        signature = inspect.signature(stage.process)
        print(signature.return_annotation)
        for name, parameter in signature.parameters.items():
            print(name, parameter.annotation)
        return True
