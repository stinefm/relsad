class Section:
    __slots__ = (
        "rank",
        "comp_list",
        "disconnectors",
        "parent",
        "child_sections",
    )

    def __init__(self, parent, comp_list, disconnectors):
        self.comp_list = comp_list
        self.disconnectors = disconnectors
        self.parent = parent
        self.child_sections = []

    def __str__(self):
        return str(self.comp_list)

    def __repr__(self):
        return f"Section({str(self.comp_list)})"

    def __eq__(self, other):
        if hasattr(other, "comp_list"):
            return set(self.comp_list) - set(other.comp_list) == set()
        else:
            return False

    def __hash__(self):
        return hash(str(self.comp_list))

    def add_child_section(self, section):
        if section not in self.child_sections:
            self.child_sections.append(section)

    def attach_to_comp(self):
        for comp in self.comp_list:
            comp.section = self
        for child_section in self.child_sections:
            child_section.attach_to_comp()
