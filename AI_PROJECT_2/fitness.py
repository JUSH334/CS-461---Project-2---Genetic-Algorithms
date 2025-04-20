from models import Assignment


def score_room_size(assignment: Assignment) -> float:
    """
    Score based on room capacity vs expected enrollment:
      - Too small: -0.5
      - Capacity >6x expected: -0.4
      - Capacity >3x expected: -0.2
      - Otherwise: +0.3
    """
    cap = assignment.room.capacity
    exp = assignment.activity.expected_enroll
    if cap < exp:
        return -0.5
    if cap > 6 * exp:
        return -0.4
    if cap > 3 * exp:
        return -0.2
    return +0.3


def score_facilitator_preference(assignment: Assignment) -> float:
    """
    Score based on facilitator suitability for the activity:
      - Preferred: +0.5
      - Other:     +0.2
      - Neither:   -0.1
    """
    fac = assignment.facilitator.name
    pref = assignment.activity.preferred
    other = assignment.activity.other
    if fac in pref:
        return 0.5
    if fac in other:
        return 0.2
    return -0.1


def activity_score(assignment: Assignment) -> float:
    """
    Combined score for a single assignment (room size + facilitator preference).
    Extend this to include other dimensions as they're implemented.
    """
    return score_room_size(assignment) + score_facilitator_preference(assignment)


def schedule_fitness(schedule: list[Assignment]) -> float:
    """
    Sum of activity scores for the entire schedule.
    """
    return sum(activity_score(a) for a in schedule)
