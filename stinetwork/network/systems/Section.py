class Section:
    __slots__ = (
        "rank",
        "comp_list",
    )

    def __init__(self, rank, comp_list):
        self.rank = rank
        self.comp_list = comp_list
        for comp in comp_list:
            comp.add_section(self)

    def __str__(self):
        return str(self.comp_list)

    def __repr__(self):
        return f"Section({str(self.comp_list)})"

    def __eq__(self, other):
        if hasattr(other, "comp_list"):
            return str(self.comp_list) == str(other.comp_list)
        else:
            return False

    def __hash__(self):
        return hash(str(self.comp_list))
