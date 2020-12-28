import numpy as np


def fix_kloppy_dataframe(pdf):
    pdf["end_timestamp"] = pdf["end_timestamp"].astype(np.float64)
    pdf["end_coordinates_x"] = pdf["end_coordinates_x"].astype(np.float64)
    pdf["end_coordinates_y"] = pdf["end_coordinates_y"].astype(np.float64)
    pdf["result"] = pdf["result"].astype(str)
    pdf["success"] = pdf["result"].astype(bool)
    if "receiver_player_id" in pdf:
        pdf["receiver_player_id"] = pdf["receiver_player_id"].astype(np.float64)
    if "pass_type" in pdf:
        pdf["pass_type"] = pdf["pass_type"].astype(str)
    pdf["set_piece_type"] = pdf["set_piece_type"].astype(str)
    if "body_part_type" in pdf:
        pdf["body_part_type"] = pdf["body_part_type"].astype(str)
    if "goalkeeper_action_type" in pdf:
        pdf["goalkeeper_action_type"] = pdf["goalkeeper_action_type"].astype(str)
    pdf["card_type"] = pdf["card_type"].astype(str)
    pdf = pdf.drop(["ball_state", "ball_owning_team"], axis=1)
    return pdf
