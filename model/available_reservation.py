from datetime import datetime

class Reservation:

    def __init__(self, date: str, time: str, place: str):
        self.date: datetime = datetime.strptime(date, "%d.%m.%Y")
        self.time: str = time
        self.place: str = place

    def __str__(self) -> str:
        return str(datetime.strftime(self.date, "%d.%m.%Y")) + ", " + self.time + ", " + self.place

    def __eq__(self, other):
        return self.date == other.date and self.time == other.time and self.place == other.place