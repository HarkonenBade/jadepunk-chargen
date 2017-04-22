import enum


class AspectTypes(enum.Enum):
    PORTRAYAL = "Portrayal"
    BACKGROUND = "Background"
    INCITING_INCIDENT = "Inciting Incident"
    BELIEF = "Belief"
    TROUBLE = "Trouble"


class Aspects(object):
    def __init__(self, **kwargs):
        self.aspects = {AspectTypes[asp.upper()]: val for asp, val in kwargs.items()}

    def validate(self, _):
        for asp in AspectTypes:
            if asp not in self.aspects:
                print("Error: Missing a {} aspect".format(asp.value))
                return False
        return True

    def render(self, engine):
        engine.heading("Aspects")
        for asp in AspectTypes:
            engine.aspect(asp.value, self.aspects[asp])
