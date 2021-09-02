class Section:
    __slots__ = (
        "rank",
        "lines",
        "disconnectors",
        "parent",
        "child_sections",
        "connected",
    )

    def __init__(self, parent, lines, disconnectors):
        self.lines = lines
        self.disconnectors = disconnectors
        self.parent = parent
        self.child_sections = []
        self.connected = True

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

    def connect(self):
        self.connected = True
        for discon in self.disconnectors:
            discon.router.close()

    def connect_manually(self):
        self.connected = True
        for discon in self.disconnectors:
            discon.close()

    def disconnect(self):
        self.connected = False
        for discon in self.disconnectors:
            discon.router.open()

    def disconnect_manually(self):
        self.connected = False
        for discon in self.disconnectors:
            discon.open()
