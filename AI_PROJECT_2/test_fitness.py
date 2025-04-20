import pytest
from models import Assignment, Room, TimeSlot, Facilitator, Activity
from fitness import score_room_size, score_facilitator_preference, activity_score

# Helper to create a dummy assignment

def make_assignment(exp_enroll, room_cap, pref_list, other_list, fac_name):
    act = Activity("TEST", exp_enroll, preferred=pref_list, other=other_list)
    room = Room("R", room_cap)
    timeslot = TimeSlot(0, "10:00")
    fac = Facilitator(fac_name)
    return Assignment(act, room, timeslot, fac)


def test_score_room_too_small():
    a = make_assignment(50, 40, [], [], "X")
    assert score_room_size(a) == pytest.approx(-0.5)


def test_score_room_medium():
    a = make_assignment(50, 100, [], [], "X")  # 100 <= 150
    assert score_room_size(a) == pytest.approx(0.3)


def test_score_room_big():
    a = make_assignment(50, 200, [], [], "X")  # 200 > 150 but <= 300
    assert score_room_size(a) == pytest.approx(-0.2)


def test_score_room_huge():
    a = make_assignment(50, 400, [], [], "X")  # 400 > 300
    assert score_room_size(a) == pytest.approx(-0.4)


def test_score_pref_preferred():
    a = make_assignment(0, 0, ["Alice"], [], "Alice")
    assert score_facilitator_preference(a) == pytest.approx(0.5)


def test_score_pref_other():
    a = make_assignment(0, 0, [], ["Bob"], "Bob")
    assert score_facilitator_preference(a) == pytest.approx(0.2)


def test_score_pref_neither():
    a = make_assignment(0, 0, [], [], "Charlie")
    assert score_facilitator_preference(a) == pytest.approx(-0.1)


def test_activity_score_combines():
    # room medium (+0.3) + preferred (+0.5) = 0.8
    a = make_assignment(10, 20, ["P"], [], "P")
    result = activity_score(a)
    assert result == pytest.approx(0.8)


def test_schedule_fitness_sum():
    a1 = make_assignment(10, 20, ["P"], [], "P")  # 0.8
    a2 = make_assignment(50, 40, [], [], "X")      # -0.5 - 0.1 = -0.6
    sched = [a1, a2]
    assert sum([0.8, -0.6]) == pytest.approx(activity_score(a1) + activity_score(a2))
    assert pytest.approx(sum([0.8, -0.6])) == pytest.approx(activity_score(a1) + activity_score(a2))
