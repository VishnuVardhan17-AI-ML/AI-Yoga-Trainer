def calculate_tree_accuracy(
    left_knee_angle,
    right_knee_angle
):

    score = 100

    if left_knee_angle > 160:
        score -= abs(left_knee_angle - 180)

    if right_knee_angle > 100:
        score -= abs(right_knee_angle - 90)

    return max(0, min(100, score))


def calculate_warrior_accuracy(
    left_knee_angle,
    right_knee_angle,
    left_elbow_angle,
    right_elbow_angle
):

    score = 100

    score -= abs(left_elbow_angle - 180) * 0.2
    score -= abs(right_elbow_angle - 180) * 0.2

    return max(0, min(100, int(score)))


def calculate_chair_accuracy(
    left_knee_angle,
    right_knee_angle,
    left_elbow_angle,
    right_elbow_angle
):

    score = 100

    score -= abs(left_knee_angle - 100) * 0.3
    score -= abs(right_knee_angle - 100) * 0.3

    score -= abs(left_elbow_angle - 180) * 0.2
    score -= abs(right_elbow_angle - 180) * 0.2

    return max(0, min(100, int(score)))