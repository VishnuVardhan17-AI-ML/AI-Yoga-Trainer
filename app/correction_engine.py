def get_pose_correction(
pose_name,
left_knee_angle,
right_knee_angle,
left_elbow_angle,
right_elbow_angle
):

 if pose_name == "TREE POSE":

    if left_knee_angle > 120 and right_knee_angle > 120:
        return "Raise one knee higher"

    return "Good Balance"

 elif pose_name == "WARRIOR POSE":

    if left_elbow_angle < 150 or right_elbow_angle < 150:
        return "Straighten both arms"

    return "Excellent Warrior Pose"

 elif pose_name == "CHAIR POSE":

    if left_knee_angle > 120 or right_knee_angle > 120:
        return "Bend knees more"

    return "Great Chair Pose"

 elif pose_name == "COBRA POSE":

    return "Lift chest slightly higher"

 return "Adjust your posture"

