import enum


class AttrTypes(enum.Enum):
    ARISTOCRAT = "Aristocrat"
    ENGINEER = "Engineer"
    EXPLORER = "Explorer"
    FIGHTER = "Fighter"
    SCHOLAR = "Scholar"
    SCOUNDREL = "Scoundrel"


class Attrs(object):
    def __init__(self, **kwargs):
        self.attrs = {AttrTypes[attr.upper()]: val for attr, val in kwargs.items()}

    def validate(self, val):
        if len(self.attrs) != 6:
            val.err("Missing attribute")

        if val.new_char:
            counts = [0]*4
            for k, a in self.attrs.items():
                if a > 3 or a < 0:
                    val.err("{} attribute is higher than 3 or less than 0".format(k.name))
                counts[a] += 1

            if counts != [1, 2, 2, 1]:
                val.err("Incorrect attribute spread.\n"
                        "Should have 1x0 2x1 2x2 1x3\n"
                        "You have {}".format(" ".join(["{}x{}".format(n, x) for x, n in enumerate(counts)])))
        else:
            for attr in AttrTypes:
                val = self.attrs[attr]
                if val < 0 or val > 5:
                    val.err("{} attribute has value {}, it should be withing 0-5".format(attr.value, val))

    def render(self, engine):
        engine.heading("Attributes")
        for attr in AttrTypes:
            engine.kv(attr.value, "+{}".format(self.attrs[attr]))
