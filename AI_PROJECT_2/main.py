import random
from models import Assignment
from data import rooms, times, facilitators, activities


def random_assignment():
    return Assignment(
        activity=random.choice(activities),
        room=random.choice(rooms),
        time_slot=random.choice(times),
        facilitator=random.choice(facilitators)
    )


def random_schedule():
    """Generate a full schedule (list of 10 assignments)."""
    return [random_assignment() for _ in activities]


if __name__ == "__main__":
    schedule = random_schedule()
    for assign in schedule:
        print(f"{assign.activity.code} | {assign.room.name} @ {assign.time_slot.label} | {assign.facilitator.name}")
