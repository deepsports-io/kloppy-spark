import numpy as np
from kloppy.domain import Dataset
from pyspark.sql import DataFrame

from ..pipeline import Pipeline
from ..stage import Source
from ..utils import kloppy_helpers as kh


class DatasetSource(Source):
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def process(self, pipeline: Pipeline, inputs=None) -> DataFrame:
        pdf = self.dataset.to_pandas(all_passes=True)
        pdf = kh.fix_kloppy_dataframe(pdf)
        return pipeline.spark.createDataFrame(pdf)
