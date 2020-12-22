import pyspark
from pyspark.sql import functions as F

from ..pipeline import Pipeline
from ..stage import Sink


class ShowDataFrame(Sink):
    def __init__(self, columns=None, tail=False, num=20):
        self.columns = columns
        self.tail = tail
        self.num = num

    def process(self, pipeline: Pipeline, inputs: pyspark.sql.DataFrame) -> None:
        if self.columns:
            df = inputs[self.columns]
        else:
            df = inputs

        if self.tail:
            df = df.withColumn("index", F.monotonically_increasing_id())
            df.orderBy(F.desc("index")).drop("index").show(self.num)
        else:
            df.show(self.num)
