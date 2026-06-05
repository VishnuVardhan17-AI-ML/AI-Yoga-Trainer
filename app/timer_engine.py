import time

pose_start_time = None


def update_timer(pose_name):

    global pose_start_time

    if pose_name == "NOT DETECTED":
        pose_start_time = None
        return 0

    if pose_start_time is None:
        pose_start_time = time.time()

    elapsed = int(time.time() - pose_start_time)

    return elapsed