from typing import List

import numpy as np
import pyspark
from kloppy import datasets
from pyspark.sql import DataFrame

from ..pipeline import Pipeline
from ..stage import Source
from ..utils import kloppy_helpers as kh


def _load_match(provider: str, match_id: str) -> List[pyspark.Row]:
    dataset = datasets.load(provider, match_id=match_id)
    pdf = kh.fix_kloppy_dataframe(dataset.to_pandas(all_passes=True))
    return [pyspark.Row(match=match_id, **row) for row in pdf.to_dict(orient="records")]


class Datasets(Source):
    def __init__(self, provider: str, matches: List[str]):
        self.matches = matches
        self.provider = provider

    def process(self, pipeline: Pipeline, inputs=None) -> DataFrame:
        return (
            pipeline.sc.parallelize(self.matches)
            .flatMap(lambda x: _load_match(self.provider, x))
            .toDF()
        )
