from kloppy.domain import Dimension
from pyspark.sql import functions as F
from pyspark.sql.types import BooleanType


class Zone:
    def __init__(self, x_dim: Dimension, y_dim: Dimension):
        self.x_dim = x_dim
        self.y_dim = y_dim

    def is_in_zone(self, x, y):
        if x >= self.x_dim.min and x <= self.x_dim.max:
            if y >= self.y_dim.min and y <= self.y_dim.max:
                return True
        return False


def filter_in_zone(zone):
    @F.udf(returnType=BooleanType())
    def wrapped(x, y):
        return zone.is_in_zone(x, y)

    return wrapped
