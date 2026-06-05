def detect_tree_pose(
    left_knee_angle,
    right_knee_angle
):

    if left_knee_angle > 160 and right_knee_angle < 100:
        return "TREE POSE"

    if right_knee_angle > 160 and left_knee_angle < 100:
        return "TREE POSE"

    return "NOT DETECTED"


def detect_warrior_pose(
    left_knee_angle,
    right_knee_angle,
    left_elbow_angle,
    right_elbow_angle
):

    if (
        80 <= left_knee_angle <= 120
        and right_knee_angle > 150
        and left_elbow_angle > 150
        and right_elbow_angle > 150
    ):
        return "WARRIOR POSE"

    if (
        80 <= right_knee_angle <= 120
        and left_knee_angle > 150
        and left_elbow_angle > 150
        and right_elbow_angle > 150
    ):
        return "WARRIOR POSE"

    return None


def detect_chair_pose(
    left_knee_angle,
    right_knee_angle,
    left_elbow_angle,
    right_elbow_angle
):

    if (
        80 <= left_knee_angle <= 130
        and 80 <= right_knee_angle <= 130
        and left_elbow_angle > 150
        and right_elbow_angle > 150
    ):
        return "CHAIR POSE"

    return None

def detect_cobra_pose(
    left_elbow_angle,
    right_elbow_angle,
    left_knee_angle,
    right_knee_angle
):

    if (
        left_elbow_angle > 150
        and right_elbow_angle > 150
        and left_knee_angle > 160
        and right_knee_angle > 160
    ):
        return "COBRA POSE"

    return None