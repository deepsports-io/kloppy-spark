from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from ..pipeline import Pipeline
from ..stage import Stage
from ..utils.zone import Zone, filter_in_zone


class PassesIntoZone(Stage):
    def __init__(self, zone: Zone, team_id: str):
        self.zone = zone
        self.team_id = team_id

    def process(self, pipeline: Pipeline, inputs: DataFrame) -> DataFrame:
        zone_filter = filter_in_zone(self.zone)
        passes = inputs \
            .filter(F.col("event_type").isin(["PASS"])) \
            .filter(F.col("team_id") == self.team_id) \
            .filter(F.col("set_piece_type") != "CORNER_KICK") \
            .filter(
                ~zone_filter(F.col("coordinates_x"), F.col("coordinates_y")) & 
                zone_filter(F.col("end_coordinates_x"), F.col("end_coordinates_y"))
            )
        return passes
