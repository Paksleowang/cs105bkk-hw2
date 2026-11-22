"""HW2 · club.py: the club and its chat bot. Practises Session 4 (each class has one job),
Session 5 (importing your own modules and the standard library) and Session 6 (catching only
the errors you expect)."""

from errors import SignupError, UnknownEventError
from event import Event
from collections import Counter


class Club:
    """A student club. It finds events by title; each Event looks after its own seats."""

    def __init__(self, name: str):
        """Provided: a club with no events yet."""
        self.name = name
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, capacity: int) -> Event:
        """Make a new Event, store it under its title, and return it."""
        if title in self.events.keys() or capacity < 1 :
            raise ValueError("Event already registered or capacity connot be less than 0.")
        self.events[title] = Event(title,capacity)
        return self.events[title]
    
    def event(self, title: str) -> Event:
        """Return the event with this title, or raise UnknownEventError."""
        if title not in self.events.keys():
            raise UnknownEventError(title)
        return self.events[title]

    def handle(self, line: str) -> str:
        """Answer one chat command, such as "join, Muay Thai basics, Nino", with one sentence."""
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3:
            return f"Sorry, I don't understand '{line}'."

        action, event, name = parts
        if action not in {"join", "leave"}:
            return f"Sorry, I don't understand '{line}'."

        try:
            if event not in self.events:
                raise UnknownEventError(event)

            club_event = self.events[event]

            if action == "join":
                if name in club_event.seats or name in club_event.waitlist:
                    raise SignupError(f"{name} is already signed up for {event}")

                if len(club_event.seats) < club_event.capacity:
                    club_event.seats.append(name)
                    return f"{name} has a seat at {event}."

                club_event.waitlist.append(name)
                return f"{name} is on the waitlist for {event}."
            
            if name not in club_event.seats:
                raise SignupError(f"{name} is not signed up for {event}")

            club_event.seats.remove(name)
            if club_event.waitlist:
                waiter = club_event.waitlist.pop(0)
                club_event.seats.append(waiter)
                return f"{name} left {event}. {waiter} gets the seat."

            return f"{name} left {event}."

        except (UnknownEventError, SignupError) as error:
            return f"Sorry, {error}."


    def attendance(self) -> dict[str, int]:
        """How many events each member has a seat at. The waitlist does not count."""
        counts = Counter()
        for event in self.events.values():
            for member in event.seats:
                counts[member] += 1
        return dict(counts)
        

if __name__ == "__main__":
    # Provided: a short run of the chat bot. It runs only with `python club.py`, not on import.
    club = Club("Harbour.Space Bangkok club")
    club.add_event("Muay Thai basics", 2)
    for line in [
        "join, Muay Thai basics, Nino",
        "join, Muay Thai basics, Aung",
        "join, Muay Thai basics, Tashi",
        "leave, Muay Thai basics, Nino",
        "join, Chess night, Ploy",
    ]:
        print(club.handle(line))
