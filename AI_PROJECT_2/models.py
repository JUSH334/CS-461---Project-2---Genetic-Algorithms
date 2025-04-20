from dataclasses import dataclass
from typing import List

@dataclass
class Room:
    name: str
    capacity: int

@dataclass
class Facilitator:
    name: str

@dataclass
class TimeSlot:
    index: int      # 0→10 AM, 1→11 AM, …, 5→3 PM
    label: str      # e.g., "10:00"

@dataclass
class Activity:
    code: str               # e.g., "SLA100A"
    expected_enroll: int
    preferred: List[str]    # names of preferred facilitators
    other: List[str]        # names of acceptable facilitators

@dataclass
class Assignment:
    activity: Activity
    room: Room
    time_slot: TimeSlot
    facilitator: Facilitator
