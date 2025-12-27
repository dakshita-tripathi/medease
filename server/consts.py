from enum import Enum

class AppointmentStatus(str, Enum):
    scheduled = "requested"
    accepted = "accepted"
    cancelled = "cancelled"
    completed = "completed"