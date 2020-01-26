class Volunteer:
    def __init__(self, tags, avail):
        self.tags = tags #["Server", "Homework"]
        self.avail = avail #[(1, "7:45", "10:00"), (3, "15:00", "17:00")]

class VolunteerEvent:
    def __init__(self, tags, time):
        self.tags = tags
        self.time = time
