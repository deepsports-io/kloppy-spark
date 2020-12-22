import numpy as np
import pyspark
from kloppy.domain import Dataset

from ..pipeline import Pipeline
from ..stage import Source


class DatasetSource(Source):
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def process(self, pipeline: Pipeline, inputs: None) -> pyspark.sql.DataFrame:
        pdf = self.dataset.to_pandas()
        pdf["end_timestamp"] = pdf["end_timestamp"].astype(np.float64)
        pdf["end_coordinates_x"] = pdf["end_coordinates_x"].astype(np.float64)
        pdf["end_coordinates_y"] = pdf["end_coordinates_y"].astype(np.float64)
        pdf["result"] = pdf["result"].astype(str)
        pdf["success"] = pdf["result"].astype(bool)
        pdf["pass_type"] = pdf["pass_type"].astype(str)
        pdf["set_piece_type"] = pdf["set_piece_type"].astype(str)
        pdf["body_part_type"] = pdf["body_part_type"].astype(str)
        pdf["goalkeeper_action_type"] = pdf["goalkeeper_action_type"].astype(str)
        pdf["card_type"] = pdf["card_type"].astype(str)

        pdf = pdf.drop(["ball_state", "ball_owning_team"], axis=1)

        return pipeline.spark.createDataFrame(pdf)

        
