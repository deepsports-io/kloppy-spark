from typing import Tuple

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from ..pipeline import Pipeline
from ..stage import Sink, Stage
from ..utils import FootballPitch


class PlotPasses(Stage):
    def process(self, pipeline: Pipeline, inputs: DataFrame) -> Tuple:
        successful_passes = inputs.filter(inputs.result == "COMPLETE").collect()
        unsuccessful_passes = inputs.filter(inputs.result != "COMPLETE").collect()

        pitch = FootballPitch()
        fig, axes = pitch.draw_pitch(scale=2)

        def plot_passes(passes, pitch, ax, width=2, color="black"):
            x_start = [p.coordinates_x for p in passes]
            y_start = [p.coordinates_y for p in passes]
            x_end = [p.end_coordinates_x for p in passes]
            y_end = [p.end_coordinates_y for p in passes]
            pitch.arrows(
                x_start, y_start, x_end, y_end, ax=axes, width=width, color=color
            )

        plot_passes(successful_passes, pitch, axes, width=1)
        plot_passes(unsuccessful_passes, pitch, axes, width=0.5, color="red")

        return fig, axes
