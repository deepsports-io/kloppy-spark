from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

from ..pipeline import Pipeline
from ..stage import Stage


class Score(Stage):
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

    def process(self, pipeline: "Pipeline", inputs: DataFrame) -> DataFrame:
        def is_goal(team_id):
            return (
                (F.col("event_type") == "SHOT")
                & (F.col("result") == "GOAL")
                & (F.col("team_id") == team_id)
            )

        windowSpec = Window.orderBy("period_id", "timestamp").rangeBetween(
            Window.unboundedPreceding, 0
        )
        home_score = F.sum(is_goal(self.home_team).cast("long")).over(windowSpec)
        away_score = F.sum(is_goal(self.away_team).cast("long")).over(windowSpec)
        score = F.concat(home_score, F.lit(":"), away_score)

        return inputs.withColumn("score", score)
