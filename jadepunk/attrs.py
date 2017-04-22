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

    def validate(self, new_char):
        if len(self.attrs) != 6:
            print("Error: Missing attribute")
            return False

        if new_char:
            counts = [0]*4
            for k, a in self.attrs.items():
                if a > 3 or a < 0:
                    print("Error: {} attribute is higher than 3 or less than 0".format(k.name))
                    return False
                counts[a] += 1

            if counts == [1, 2, 2, 1]:
                return True
            else:
                print("Error: Incorrect attribute spread.")
                print("Should have 1x0 2x1 2x2 1x3")
                print("You have {}".format(
                    " ".join(
                        ["{}x{}".format(n, x)
                         for x, n in enumerate(counts)]
                    )
                ))
                return False
        else:
            valid = True
            for attr in AttrTypes:
                val = self.attrs[attr]
                if val < 0 or val > 5:
                    print("Error: {} attribute has value {}, it should be withing 0-5".format(attr.value,
                                                                                              val))
                    valid = False
            return valid

    def render(self, engine):
        engine.heading("Attributes")
        for attr in AttrTypes:
            engine.kv(attr.value, "+{}".format(self.attrs[attr]))
