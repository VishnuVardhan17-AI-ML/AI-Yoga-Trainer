def calculate_tree_accuracy(
    left_knee_angle,
    right_knee_angle
):

    score = 0

    if left_knee_angle > 160:
        score += 50

    if right_knee_angle < 100:
        score += 50

    return score


def calculate_warrior_accuracy(
    left_knee_angle,
    right_knee_angle,
    left_elbow_angle,
    right_elbow_angle
):

    score = 0

    if 80 <= left_knee_angle <= 120:
        score += 25

    if right_knee_angle > 150:
        score += 25

    if left_elbow_angle > 150:
        score += 25

    if right_elbow_angle > 150:
        score += 25

    return score