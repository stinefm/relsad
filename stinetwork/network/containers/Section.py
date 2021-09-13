from enum import Enum
from stinetwork.utils import Time


class SectionState(Enum):
    CONNECTED = 1
    DISCONNECTED = 2


class Section:
    __slots__ = (
        "rank",
        "lines",
        "disconnectors",
        "parent",
        "child_sections",
        "state",
    )

    def __init__(self, parent, lines, disconnectors):
        self.lines = lines
        self.disconnectors = disconnectors
        self.parent = parent
        self.child_sections = []
        self.state = SectionState.CONNECTED

    def __str__(self):
        return str(self.lines)

    def __repr__(self):
        return f"Section({str(self.lines)})"

    def __eq__(self, other):
        if hasattr(other, "lines"):
            return set(self.lines) - set(other.lines) == set()
        else:
            return False

    def __hash__(self):
        return hash(str(self.lines))

    def add_child_section(self, section):
        if section not in self.child_sections:
            self.child_sections.append(section)

    def attach_to_lines(self):
        for line in self.lines:
            line.section = self
        for child_section in self.child_sections:
            child_section.attach_to_lines()

    def connect(self, dt: Time):
        self.state = SectionState.CONNECTED
        for line in self.lines:
            line.connect()
        for discon in self.disconnectors:
            discon.intelligent_switch.close(dt)

    def connect_manually(self):
        self.state = SectionState.CONNECTED
        for line in self.lines:
            line.connect()
        for discon in self.disconnectors:
            discon.close()

    def disconnect(self, dt: Time):
        section_time = Time(0)
        self.state = SectionState.DISCONNECTED
        for line in self.lines:
            line.disconnect()
        for discon in self.disconnectors:
            section_time += discon.intelligent_switch.open(dt)
        return section_time

    def disconnect_manually(self):
        self.state = SectionState.DISCONNECTED
        for line in self.lines:
            line.disconnect()
        for discon in self.disconnectors:
            discon.open()
