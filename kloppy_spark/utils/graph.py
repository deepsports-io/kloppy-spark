from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, List


class Graph:
    def __init__(self):
        self.vertices = {}
        self.graph = defaultdict(list)

    def add_vertex(self, name: str, data: "Stage") -> None:
        self.vertices[name] = data

    def add_edge(self, source: str, dest: str) -> None:
        self.graph[source].append(dest)

    def _topological_sort_util(self, prev_key, key, stage, visited, stack) -> None:
        visited[key] = True

        for next_stage in self.graph[key]:
            if not visited[next_stage]:
                self._topological_sort_util(
                    key, next_stage, self.vertices[next_stage], visited, stack
                )

        stack.insert(0, (prev_key, key, stage))

    def topological_sort(self) -> List:
        visited = dict([(k, False) for k in self.vertices.keys()])
        stack = []

        for k, stage in self.vertices.items():
            if not visited[k]:
                self._topological_sort_util(None, k, stage, visited, stack)

        return stack
