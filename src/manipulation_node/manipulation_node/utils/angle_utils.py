from math import atan2, pi, sin, cos


def calculate_arm_angles(shoulder, elbow, wrist):
    """
    Calculate shoulder and elbow joint commands from keypoint positions.

    Args:
        shoulder: (x, y) tuple for shoulder keypoint
        elbow: (x, y) tuple for elbow keypoint
        wrist: (x, y) tuple for wrist keypoint

    Returns:
        tuple: (shoulder_cmd, elbow_cmd) in radians
    """
    a1 = atan2(-(elbow[1] - shoulder[1]), (elbow[0] - shoulder[0]))
    a2 = atan2(-(wrist[1] - elbow[1]),    (wrist[0] - elbow[0]))
    a1 = atan2(sin(a1), cos(a1))

    relative = a2 - a1
    relative = atan2(sin(relative), cos(relative))

    shoulder_cmd = atan2(
        (elbow[1] - shoulder[1]),
        abs(elbow[0] - shoulder[0])
    )
    elbow_cmd = -pi/2 - relative

    return shoulder_cmd, elbow_cmd
