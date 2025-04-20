from models import Room, Facilitator, TimeSlot, Activity

# Rooms
rooms = [
    Room("Slater 003", 45),
    Room("Roman 216", 30),
    Room("Loft 206", 75),
    Room("Roman 201", 50),
    Room("Loft 310", 108),
    Room("Beach 201", 60),
    Room("Beach 301", 75),
    Room("Logos 325", 450),
    Room("Frank 119", 60),
]

# Time slots
times = [
    TimeSlot(i, f"{10+i}:00") for i in range(6)
]

# Facilitators
facilitators = [
    Facilitator(name) for name in
    ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"]
]

# Activities
activities = [
    Activity("SLA100A", 50, preferred=["Glen","Lock","Banks","Zeldin"], other=["Numen","Richards"]),
    Activity("SLA100B", 50, preferred=["Glen","Lock","Banks","Zeldin"], other=["Numen","Richards"]),
    Activity("SLA191A", 50, preferred=["Glen","Lock","Banks","Zeldin"], other=["Numen","Richards"]),
    Activity("SLA191B", 50, preferred=["Glen","Lock","Banks","Zeldin"], other=["Numen","Richards"]),
    Activity("SLA201" , 50, preferred=["Glen","Banks","Zeldin","Shaw"], other=["Numen","Richards","Singer"]),
    Activity("SLA291" , 50, preferred=["Lock","Banks","Zeldin","Singer"], other=["Numen","Richards","Shaw","Tyler"]),
    Activity("SLA303" , 60, preferred=["Glen","Zeldin","Banks"], other=["Numen","Singer","Shaw"]),
    Activity("SLA304" , 25, preferred=["Glen","Banks","Tyler"], other=["Numen","Singer","Shaw","Richards","Uther","Zeldin"]),
    Activity("SLA394" , 20, preferred=["Tyler","Singer"], other=["Richards","Zeldin"]),
    Activity("SLA449" , 60, preferred=["Tyler","Singer","Shaw"], other=["Zeldin","Uther"]),
    Activity("SLA451" ,100, preferred=["Tyler","Singer","Shaw"], other=["Zeldin","Uther","Richards","Banks"]),
]
