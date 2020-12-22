from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

from ..pipeline import Pipeline
from ..stage import Stage

OPEN_SEQUENCE = ["PASS", "CARRY", "RECOVERY"]
CLOSE_SEQUENCE = ["BALL_OUT", "FOUL_COMMITTED", "SHOT"]


class Sequences(Stage):
    def process(self, pipeline: "Pipeline", inputs: DataFrame) -> DataFrame:
        windowSpec = Window.orderBy("period_id", "timestamp")
        return (
            inputs.withColumn(
                "seq", F.lag(F.col("team_id")).over(windowSpec) != F.col("team_id")
            )
            .withColumn(
                "seq",
                (F.col("event_type").isin(OPEN_SEQUENCE) & F.col("seq"))
                | F.col("event_type").isin(CLOSE_SEQUENCE),
            )
            .withColumn("seq_no", F.sum(F.col("seq").cast("long")).over(windowSpec))
            .rdd.map(lambda e: (e.seq_no, e))
            .groupByKey()
            .mapValues(list)
            .filter(
                lambda k: len(list(filter(lambda x: x.event_type == "PASS", k[1]))) > 10
            )
            .toDF()
        )
