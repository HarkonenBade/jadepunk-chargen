# -*- coding: UTF-8 -*-

import enum


class Character(object):
    def __init__(self,
                 name,
                 aspects,
                 attrs,
                 assets,
                 max_refresh=7,
                 new_gen=True):
        """

        :rtype: Character
        """
        self.name = name
        self.aspects = aspects
        self.attrs = attrs
        self.assets = assets
        self.max_ref = max_refresh
        if not self.validate(new_gen):
            print("\n\n==============INVALID CHAR==============\n")

    def refresh(self):
        return self.max_ref - sum([asset.refresh() for asset in self.assets])

    def validate(self, new_char):
        valid = True
        if self.name == "":
            print("Error: Character must have a name.")
            valid = False

        valid = (self.aspects.validate(new_char) and
                 self.attrs.validate(new_char) and
                 all([asset.validate(new_char) for asset in self.assets]) and
                 valid)

        if new_char and self.max_ref != 7:
            print("Error: Starting chars have 7 refresh max")
            valid = False
        if self.refresh() <= 1:
            print("Error: Char cannot have 0 or negative refresh")
            valid = False
        return valid

    def render_stats(self, engine):
        with engine.section():
            engine.heading("Stats")
            engine.kv("Refresh", self.refresh())
            engine.kv("Stress", "")
            engine.kv("Mild Consequence", "")
            engine.kv("Major Consequence", "")
            engine.kv("Severe Consequence", "")

    def render(self, engine):
        with engine.section():
            engine.title(self.name)
        self.aspects.render(engine)
        self.attrs.render(engine)
        self.render_stats(engine)
        engine.heading("Assets")
        for asset in self.assets:
            asset.render(engine)


class Aspects(object):
    class Types(enum.Enum):
        PORTRAYAL = "Portrayal"
        BACKGROUND = "Background"
        INCITING_INCIDENT = "Inciting Incident"
        BELIEF = "Belief"
        TROUBLE = "Trouble"

    def __init__(self, **kwargs):
        """

        :rtype: Aspects
        """
        self.aspects = {self.Types[asp.upper()]: val for asp, val in kwargs.items()}

    def validate(self, _):
        for asp in self.Types:
            if asp not in self.aspects:
                print("Error: Missing a {} aspect".format(asp.value))
                return False
        return True

    def render(self, engine):
        with engine.section():
            engine.heading("Aspects")
            for asp in self.Types:
                engine.aspect(asp.value, self.aspects[asp])


class Attrs(object):
    class Types(enum.Enum):
        ARISTOCRAT = "Aristocrat"
        ENGINEER = "Engineer"
        EXPLORER = "Explorer"
        FIGHTER = "Fighter"
        SCHOLAR = "Scholar"
        SCOUNDREL = "Scoundrel"

    def __init__(self, **kwargs):
        """

        :rtype: Attrs
        """
        self.attrs = {self.Types[attr.upper()]: val for attr, val in kwargs.items()}

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

            if(counts[0] == 1 and
               counts[1] == 2 and
               counts[2] == 2 and
               counts[3] == 1):
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
            for attr in self.Types:
                val = self.attrs[attr]
                if val < 0 or val > 5:
                    print("Error: {} attribute has value {}, it should be withing 0-5".format(attr.value,
                                                                                              val))
                    valid = False
            return valid

    def render(self, engine):
        with engine.section():
            engine.heading("Attributes")
            for attr in self.Types:
                engine.kv(attr.value, "+{}".format(self.attrs[attr]))


class Asset(object):
    class Types(enum.Enum):
        DEVICE = "Device"
        TECH = "Technique"
        ALLY = "Ally"

    class Prop(object):
        def name(self):
            return type(self).__name__

        @staticmethod
        def _err(master, txt, *args):
            print("Error: Asset {}: {}".format(master.name(), txt.format(*args)))

        def _type_restrict(self, master, types):
            if master.type not in types:
                self._err(master,
                          "Can only apply {} feature to {}",
                          self.name(),
                          " and ".join([t.value for t in types]))
                return False
            return True

        def _req_situational(self, master):
            if not any([isinstance(f, Asset.Situational) for f in master.flaws]):
                self._err(master, "{} requires Situational", self.name())
                return False
            return True

        def validate(self, _):
            return True

        def cost(self, _):
            if hasattr(self, "ranks"):
                return self.ranks, False
            return 1, False

    class Aspect(Prop):
        def __init__(self, aspect):
            self.aspect = aspect

        def render(self, engine):
            return "{} ({})".format(engine.italics("Aspect"), engine.boldit(self.aspect))

        def validate(self, master):
            if self.aspect == "":
                self._err(master, "Missing details for Aspect.")
                return False
            return self._type_restrict(master, [Asset.Types.ALLY, Asset.Types.DEVICE])

    class Exceptional(Prop):
        def __init__(self, txt):
            self.txt = txt

        def render(self, engine):
            return "{} ({})".format(engine.italics("Exceptional"), self.txt)

        def validate(self, master):
            return self._type_restrict(master, [Asset.Types.DEVICE, Asset.Types.TECH])

        def cost(self, _):
            return 2, True

    class Flexible(Prop):
        def __init__(self, replacing, replaced):
            self.replacing = replacing
            self.replaced = replaced

        def render(self, engine):
            return "{} (Use {} instead of {})".format(engine.italics("Flexible"),
                                                      self.replacing.value,
                                                      self.replaced.value)

        def validate(self, master):
            if self.replacing == self.replaced:
                self._err(master, "Replacing and Replaced must be different")
                return False
            return self._req_situational(master) and self._type_restrict(master, [Asset.Types.DEVICE, Asset.Types.TECH])

        def cost(self, _):
            return 2, False

    class Focus(Prop):
        def __init__(self, attr, ranks=1):
            self.attr = attr
            self.ranks = ranks

        def render(self, engine):
            return "{t} {r} ({a} +{r})".format(t=engine.italics("Focus"), r=self.ranks, a=self.attr.value)

        def validate(self, master):
            return self._req_situational(master) and self._type_restrict(master, [Asset.Types.DEVICE, Asset.Types.TECH])

    class Harmful(Prop):
        def __init__(self, ranks):
            self.ranks = ranks

        def render(self, engine):
            return "{} {}".format(engine.italics("Harmful"), self.ranks)

        def validate(self, master):
            return self._type_restrict(master, [Asset.Types.DEVICE, Asset.Types.TECH])

    class Independent(Prop):
        def __init__(self):
            pass

        def render(self, engine):
            return engine.italics("Independent")

        def validate(self, master):
            return self._type_restrict(master, [Asset.Types.ALLY])

    class Numerous(Prop):
        def __init__(self, ranks):
            self.ranks = ranks

        def render(self, engine):
            return "{} {} ({} copies)".format(engine.italics("Numerous"), self.ranks, 2**self.ranks)

        def validate(self, master):
            return self._type_restrict(master, [Asset.Types.ALLY, Asset.Types.DEVICE])

    class Professional(Prop):
        def __init__(self, ranks, avg=None, fair=None):
            self.ranks = ranks
            self.avg = avg
            self.fair = fair

        def render(self, engine):
            if self.ranks == 1:
                txt = "{} +1".format(self.avg.value)
            else:
                txt = "{} +2, {} +1".format(self.fair.value, "+1, ".join([a.value for a in self.avg]))
            return "{} {} ({})".format(engine.italics("Professional"), self.ranks, txt)

        def validate(self, master):
            if self.ranks > 3:
                self._err(master, "No Ally may have more than 3 ranks of Professional")
                return False
            if self.ranks == 1 and (self.fair is not None or self.avg is None or not isinstance(self.avg, Attrs.Types)):
                self._err(master, "Professional 1 must have a single profession at average (+1)")
                return False
            if self.ranks == 2 and (self.fair is None or self.avg is None or len(self.avg) != 1):
                self._err(master, "Professional 2 must have a single profession at fair (+2)"
                                  "and a single at average (+1)")
                return False
            if self.ranks == 3 and (self.fair is None or self.avg is None or len(self.avg) != 3):
                self._err(master, "Professional 3 must have a single profession at fair (+2) and three at average (+1)")
                return False
            return self._type_restrict(master, [Asset.Types.ALLY])

        def cost(self, _):
            return self.ranks-1, False

    class Protective(Prop):
        def __init__(self, ranks):
            self.ranks = ranks

        def render(self, engine):
            return "{} {}".format(engine.italics("Protective"), self.ranks)

        def validate(self, master):
            if self.ranks > 2 and master.type == Asset.Types.DEVICE:
                self._err(master, "Protective may not be applied to a device more than twice")
                return False
            return self._type_restrict(master, [Asset.Types.DEVICE, Asset.Types.TECH])

        def cost(self, master):
            return self.ranks*2, master.type == Asset.Types.TECH

    class Resilient(Prop):
        def __init__(self, ranks):
            self.ranks = ranks

        def render(self, engine):
            return "{} {}".format(engine.italics("Resilient"), self.ranks)

        def validate(self, master):
            if self.ranks > 2:
                self._err(master, "Resilient may not be applied to an Ally more than twice")
                return False
            return self._type_restrict(master, [Asset.Types.ALLY])

        def cost(self, _):
            return self.ranks-1, False

    class Sturdy(Prop):
        def __init__(self, ranks):
            self.ranks = ranks

        def render(self, engine):
            return "{} {}".format(engine.italics("Sturdy"), self.ranks)

        def validate(self, master):
            if self.ranks > 3 and master.type == Asset.Types.ALLY:
                self._err(master, "Sturdy may not be applied to an Ally more than three times")
                return False
            if self.ranks > 2 and master.type == Asset.Types.DEVICE:
                self._err(master, "Sturdy may not be applied to a Device more than twice")
                return False
            return self._type_restrict(master, [Asset.Types.ALLY, Asset.Types.DEVICE])

        def cost(self, master):
            return self.ranks-1 if master.type == Asset.Types.ALLY else self.ranks, False

    class Talented(Prop):
        def __init__(self, a_type, prop):
            self.fake_type = a_type
            self.prop = prop

        def render(self, engine):
            return "{} {} ({})".format(engine.italics("Talented"),
                                       self.cost(None),
                                       self.prop.render(engine))

        def _fake_master(self, master):
            if master is None:
                return Asset(self.fake_type,
                             features=[],
                             flaws=[])
            else:
                return Asset(self.fake_type,
                             features=master.features,
                             flaws=master.flaws,
                             functional=master.functional,
                             name=master.name())

        def validate(self, master):
            fake_master = self._fake_master(master)
            return self._type_restrict(master, [Asset.Types.ALLY]) and self.prop.validate(fake_master)

        def cost(self, master):
            fake_master = self._fake_master(master)
            return self.prop.cost(fake_master)

    class Consuming(Prop):
        def __init__(self):
            pass

        def render(self, engine):
            return "{} (Costs a fate point to activate)".format(engine.italics("Consuming"))

        def cost(self, _):
            return 2, False

    class Demanding(Prop):
        def __init__(self, ranks, attr):
            self.ranks = ranks
            self.attr = attr

        def render(self, engine):
            if self.ranks == 1:
                txt = "One Action or A Fair (+2) {} roll".format(self.attr.value)
            else:
                txt = ("One Action and A Fair (2) {a} roll,"
                       "One Scene, or A Great (+4) {a} roll").format(a=self.attr.value)
            return "{} {} ({})".format(engine.italics("Demanding"), self.ranks, txt)

        def validate(self, master):
            if self.ranks > 2:
                self._err(master, "Cannot apply Demanding more than twice to a given Asset")
                return False
            return True

    class Limited(Prop):
        def __init__(self, ranks):
            self.ranks = ranks

        def render(self, engine):
            return "{} {} ({})".format(engine.italics("Limited"),
                                       self.ranks,
                                       "Once per scene" if self.ranks == 1 else "Once per session")

        def validate(self, master):
            if self.ranks > 2:
                self._err(master, "Cannot apply Limited more than twice to a given Asset")
                return False
            return True

    class Situational(Prop):
        def __init__(self, aspect):
            self.aspect = aspect

        def render(self, engine):
            return "{} ({})".format(engine.italics("Situational"), engine.boldit(self.aspect))

    class Troubling(Prop):
        def __init__(self, aspect):
            self.aspect = aspect

        def render(self, engine):
            return "{} ({})".format(engine.italics("Troubling"), engine.boldit(self.aspect))

    def __init__(self,
                 a_type,
                 features,
                 flaws,
                 functional=None,
                 guiding=None,
                 name=None,
                 gm_approved=False):
        """
        :type a_type: Asset.Types
        :type features: list
        :type flaws: list
        :type functional: str
        :type guiding: str
        :type name: str
        :rtype: Asset
        """
        self.type = a_type
        self.features = features
        self.flaws = flaws
        self.functional = functional
        self.guiding = guiding
        self.raw_name = name
        self.silence_gm = gm_approved

    def name(self):
        if self.raw_name is not None:
            return self.raw_name
        else:
            return self.functional

    def refresh(self):
        features = 0
        flaws = 0
        more_starting_flaws = False
        for f in self.features:
            dfet, mflaws = f.cost(self)
            features += dfet
            more_starting_flaws = more_starting_flaws or mflaws
        for f in self.flaws:
            dflaw, _ = f.cost(self)
            flaws += dflaw
        if more_starting_flaws:
            return max((features - (flaws - 2)) // 2, 1)
        else:
            return max((features - (flaws - 1)) // 2, 1)

    def validate(self, new_char):
        return all([f.validate(self) for f in self.features + self.flaws])

    def render(self, engine):
        engine.subheading(self.name())
        engine.kv("Type", self.type.value)
        if self.functional is not None:
            if self.raw_name is not None:
                engine.aspect("Functional Aspect", self.functional)
        if self.guiding is not None:
            engine.aspect("Guiding Aspect", self.guiding)
        engine.kv("Features", ", ".join([f.render(engine) for f in self.features]))
        engine.kv("Flaws", ", ".join([f.render(engine) for f in self.flaws]))
        engine.kv("Cost", self.refresh())
