from abc import ABC, abstractmethod
from typing import Any


class Stage(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def process(self, pipeline: "Pipeline", inputs: Any) -> Any:
        pass


class Source(Stage):
    @abstractmethod
    def process(self, pipeline: "Pipeline", inputs: None) -> Any:
        pass


class Sink(Stage):
    @abstractmethod
    def process(self, pipeline: "Pipeline", inputs: Any) -> None:
        pass
