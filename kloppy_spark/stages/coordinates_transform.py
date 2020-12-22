from kloppy.domain import PitchDimensions
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from ..pipeline import Pipeline
from ..stage import Stage


def to_base(column, min_val, max_val):
    return (column - min_val) / (max_val - min_val)


def from_base(column, min_val, max_val):
    return (column * (max_val - min_val)) + min_val


class CoordinateTransformer(Stage):
    def __init__(self, from_dim: PitchDimensions, to_dim: PitchDimensions):
        self.from_dim = from_dim
        self.to_dim = to_dim

    def process(self, pipeline: Pipeline, inputs: DataFrame) -> DataFrame:
        result = (
            inputs.withColumn(
                "coordinates_x",
                from_base(to_base(F.col("coordinates_x"), 0, 100), 0, 105),
            )
            .withColumn(
                "coordinates_y",
                from_base(to_base(F.col("coordinates_y"), 0, 100), 0, 68),
            )
            .withColumn(
                "end_coordinates_x",
                from_base(to_base(F.col("end_coordinates_x"), 0, 100), 0, 105),
            )
            .withColumn(
                "end_coordinates_y",
                from_base(to_base(F.col("end_coordinates_y"), 0, 100), 0, 68),
            )
        )
        return result
