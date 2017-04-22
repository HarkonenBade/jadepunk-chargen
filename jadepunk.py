# -*- coding: UTF-8 -*-

import enum
import math


class AssetTypes(enum.Enum):
    DEVICE = "Device"
    TECH = "Technique"
    ALLY = "Ally"


class AttrTypes(enum.Enum):
    ARISTOCRAT = "Aristocrat"
    ENGINEER = "Engineer"
    EXPLORER = "Explorer"
    FIGHTER = "Fighter"
    SCHOLAR = "Scholar"
    SCOUNDREL = "Scoundrel"


class AspectTypes(enum.Enum):
    PORTRAYAL = "Portrayal"
    BACKGROUND = "Background"
    INCITING_INCIDENT = "Inciting Incident"
    BELIEF = "Belief"
    TROUBLE = "Trouble"


class Character(object):
    def __init__(self,
                 name,
                 aspects,
                 attrs,
                 assets,
                 background=None,
                 max_refresh=7,
                 new_gen=True):
        self.name = name
        self.aspects = aspects
        self.attrs = attrs
        self.assets = assets
        self.max_ref = max_refresh
        self.background = background
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

    def render_background(self, engine):
        if self.background is not None:
            engine.heading("Background")
            engine.text(self.background)

    def render_stats(self, engine):
        engine.heading("Stats")
        engine.kv("Refresh", self.refresh())
        engine.kv("Stress", "")
        engine.kv("Mild Consequence", "")
        engine.kv("Major Consequence", "")
        engine.kv("Severe Consequence", "")

    def render(self, engine):
        engine.title(self.name)
        self.render_background(engine)
        self.aspects.render(engine)
        self.attrs.render(engine)
        self.render_stats(engine)
        engine.heading("Assets")
        for asset in self.assets:
            asset.render(engine)


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


class Asset(object):
    class Prop(object):
        allowed_types = []

        def __init__(self):
            self.master = None
            self.extra_flaw = False

        def set_master(self, master):
            self.master = master

        def name(self):
            return type(self).__name__

        def err(self, txt, *args):
            return self.master.err(" Property ({}): {}", self.name(), txt.format(*args))

        def _type_restrict(self):
            if len(self.allowed_types) > 0 and self.master.type not in self.allowed_types:
                return self.err("Can only be applied to {}",
                                " and ".join([t.value for t in self.allowed_types]))
            return True

        def _req_situational(self):
            if not self.master.has_prop(Asset.Situational):
                return self.err("Requires Situational")
            return True

        def render(self, engine):
            if hasattr(self, "ranks"):
                if hasattr(self, "desc"):
                    return "{} {} ({})".format(engine.italics(self.name()),
                                               self.ranks,
                                               self.desc(engine))
                else:
                    return "{} {}".format(engine.italics(self.name()),
                                          self.ranks)
            else:
                if hasattr(self, "desc"):
                    return "{} ({})".format(engine.italics(self.name()),
                                            self.desc(engine))
                else:
                    return "{}".format(engine.italics(self.name()))

        def validate(self):
            return self._type_restrict()

        def additional_flaw(self):
            return self.extra_flaw

        def cost(self):
            if hasattr(self, "ranks"):
                return self.ranks
            return 1

    class Feature(Prop):
        pass

    class Flaw(Prop):
        pass

    class Aspect(Feature):
        allowed_types = [AssetTypes.ALLY, AssetTypes.DEVICE]

        def __init__(self, aspect):
            super().__init__()
            self.aspect = aspect

        def desc(self, engine):
            return engine.boldit(self.aspect)

        def validate(self):
            if self.aspect == "":
                return self.err("Missing details for Aspect.")
            return super().validate()

    class Exceptional(Feature):
        def __init__(self, txt):
            super().__init__()
            self.txt = txt
            self.extra_flaw = True

        def desc(self, _):
            return self.txt

        def cost(self):
            return 2

    class Flexible(Feature):
        allowed_types = [AssetTypes.DEVICE, AssetTypes.TECH]

        def __init__(self, replacing, replaced):
            super().__init__()
            self.replacing = replacing
            self.replaced = replaced

        def desc(self, _):
            return "Use {} instead of {}".format(self.replacing.value, self.replaced.value)

        def validate(self):
            if self.replacing == self.replaced:
                return self.err("Replacing and Replaced must be different")
            return all([self._req_situational(), super().validate()])

        def cost(self):
            return 2

    class Focus(Feature):
        allowed_types = [AssetTypes.DEVICE, AssetTypes.TECH]

        def __init__(self, attr, ranks=1):
            super().__init__()
            self.attr = attr
            self.ranks = ranks

        def desc(self, _):
            return "{} +{}".format(self.attr.value, self.ranks)

        def validate(self):
            return all([self._req_situational(), super().validate()])

    class Harmful(Feature):
        allowed_types = [AssetTypes.DEVICE, AssetTypes.TECH]

        def __init__(self, ranks):
            super().__init__()
            self.ranks = ranks

    class Independent(Feature):
        allowed_types = [AssetTypes.ALLY]

    class Numerous(Feature):
        allowed_types = [AssetTypes.ALLY, AssetTypes.DEVICE]

        def __init__(self, ranks):
            super().__init__()
            self.ranks = ranks

        def desc(self, _):
            return "{} copies".format(2**self.ranks)

    class Professional(Feature):
        allowed_types = [AssetTypes.ALLY]

        def __init__(self, ranks, avg=None, fair=None):
            super().__init__()
            self.ranks = ranks
            self.avg = avg
            self.fair = fair

        def desc(self, _):
            if self.ranks == 1:
                return "{} +1".format(self.avg.value)
            else:
                if self.ranks == 2:
                    avg = self.avg.value
                else:
                    avg = "+1, ".join([a.value for a in self.avg])
                return "{} +2, {} +1".format(self.fair.value, avg)

        def validate(self):
            if self.ranks > 3:
                return self.err("No Ally may have more than 3 ranks of Professional")
            if self.ranks == 1 and (self.fair is not None or
                                    self.avg is None or
                                    not isinstance(self.avg, AttrTypes)):
                return self.err("Professional 1 must have a single profession at average (+1)")
            if self.ranks == 2 and (self.fair is None or
                                    self.avg is None or
                                    not isinstance(self.avg, AttrTypes) or
                                    not isinstance(self.fair, AttrTypes)):
                return self.err("Professional 2 must have a single profession at fair (+2) "
                                "and a single at average (+1)")
            if self.ranks == 3 and (self.fair is None or
                                    self.avg is None or
                                    not isinstance(self.avg, list) or
                                    not isinstance(self.fair, AttrTypes) or
                                    len(self.avg) != 3):
                return self.err("Professional 3 must have a single profession at fair (+2) "
                                "and three at average (+1)")
            return super().validate()

        def cost(self):
            return self.ranks-1

    class Protective(Feature):
        allowed_types = [AssetTypes.DEVICE, AssetTypes.TECH]

        def __init__(self, ranks):
            super().__init__()
            self.ranks = ranks
            self.extra_flaw = self.master.type == AssetTypes.TECH

        def validate(self):
            if self.ranks > 2 and self.master.type == AssetTypes.DEVICE:
                return self.err("May not be applied to a device more than twice")
            return super().validate()

        def cost(self):
            return self.ranks*2

    class Resilient(Feature):
        allowed_types = [AssetTypes.ALLY]

        def __init__(self, ranks):
            super().__init__()
            self.ranks = ranks

        def validate(self):
            if self.ranks > 2:
                return self.err("May not be applied to an Ally more than twice")
            return super().validate()

        def cost(self):
            return self.ranks-1

    class Sturdy(Feature):
        allowed_types = [AssetTypes.ALLY, AssetTypes.DEVICE]

        def __init__(self, ranks):
            super().__init__()
            self.ranks = ranks

        def validate(self):
            if self.ranks > 3 and self.master.type == AssetTypes.ALLY:
                return self.err("May not be applied to an Ally more than three times")
            if self.ranks > 2 and self.master.type == AssetTypes.DEVICE:
                return self.err("May not be applied to a Device more than twice")
            return super().validate()

        def cost(self):
            return self.ranks-1 if self.master.type == AssetTypes.ALLY else self.ranks

    class Talented(Feature):
        allowed_types = [AssetTypes.ALLY]

        def __init__(self, a_type, prop):
            super().__init__()
            self.fake_type = a_type
            self.prop = prop
            self.ranks = 0

        def set_master(self, master):
            super().set_master(master)
            self.prop.set_master(self._fake_master())
            self.ranks = self.prop.cost()

        def desc(self, engine):
            return self.prop.render(engine)

        def _fake_master(self):
            fake = Asset(self.fake_type,
                         features=[],
                         flaws=[],
                         functional=self.master.functional,
                         name=self.master.name())
            fake.properties = self.master.properties
            return fake

        def validate(self):
            return super().validate() and self.prop.validate()

        def additional_flaw(self):
            return self.prop.additional_flaw()

    class Consuming(Flaw):
        def __init__(self):
            super().__init__()

        @staticmethod
        def desc(_):
            return "Costs a fate point to activate"

        def cost(self):
            return 2

    class Demanding(Flaw):
        def __init__(self, ranks, attr):
            super().__init__()
            self.ranks = ranks
            self.attr = attr

        def render(self, _):
            if self.ranks == 1:
                return "One Action or A Fair (+2) {} roll".format(self.attr.value)
            else:
                return ("One Action and A Fair (2) {a} roll,"
                        "One Scene, or A Great (+4) {a} roll").format(a=self.attr.value)

        def validate(self):
            if self.ranks > 2:
                return self.err("Cannot apply Demanding more than twice to a given Asset")
            return True

    class Limited(Flaw):
        def __init__(self, ranks):
            super().__init__()
            self.ranks = ranks

        def desc(self, _):
            return "Once per scene" if self.ranks == 1 else "Once per session"

        def validate(self):
            if self.ranks > 2:
                return self.err("Cannot apply Limited more than twice to a given Asset")
            return True

    class Situational(Flaw):
        def __init__(self, aspect):
            super().__init__()
            self.aspect = aspect

        def desc(self, engine):
            return engine.boldit(self.aspect)

    class Troubling(Flaw):
        allowed_types = [AssetTypes.ALLY, AssetTypes.DEVICE]

        def __init__(self, aspect):
            super().__init__()
            self.aspect = aspect

        def desc(self, engine):
            return engine.boldit(self.aspect)

    def __init__(self,
                 a_type,
                 features,
                 flaws,
                 functional=None,
                 guiding=None,
                 name=None,
                 mastercrafted=False,
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
        self.properties = features + flaws
        self.functional = functional
        self.guiding = guiding
        self.raw_name = name
        self.silence_gm = gm_approved
        self.mastercrafted = mastercrafted

        if self.type == AssetTypes.ALLY:
            if not self.has_prop(Asset.Sturdy):
                self.properties.append(Asset.Sturdy(1))
            if not self.has_prop(Asset.Resilient):
                self.properties.append(Asset.Resilient(1))

        for p in self.properties:
            p.set_master(self)

    def _msg(self, grade, txt, *args):
        print("{}: Asset ({}): {}".format(grade, self.name(), txt.format(*args)))

    def err(self, txt, *args):
        self._msg("Error", txt, *args)
        return False

    def warn(self, txt, *args):
        self._msg("Warning", txt, *args)

    def name(self):
        if self.raw_name is not None:
            return self.raw_name
        else:
            return "Unnamed {}".format(self.type.value)

    def has_prop(self, a_type):
        return any([isinstance(f, a_type) for f in self.properties])

    def refresh(self, check=False):
        features = sum([f.cost() for f in self.features()])
        flaws = sum([f.cost() for f in self.flaws()])
        starting_flaws = 2 if any([f.additional_flaw() for f in self.properties]) else 1
        starting_features = 2

        if check and flaws < starting_flaws:
            return self.err("Must have at least {} flaws.", starting_flaws)

        fet_from_flaw = flaws - starting_flaws

        if check and features < starting_features:
            self.warn("Assets start with {} features, currently only has {}", starting_features, features)

        if check and (features - starting_features) < fet_from_flaw:
            self.warn("Can have upto {} features from flaws, currently only has {}.",
                      fet_from_flaw,
                      features - starting_features)

        fet_from_ref = features - fet_from_flaw

        if check and fet_from_ref % 2 == 1:
            self.warn("You are gaining {} features from refresh, you could gain {} for the same cost.",
                      fet_from_ref, fet_from_ref + 1)

        ref = max(math.ceil(fet_from_ref / 2), 1)
        if self.mastercrafted:
            ref = max(ref - 1, 1)
        if check:
            return True
        return ref

    def features(self):
        return [f for f in self.properties if isinstance(f, Asset.Feature)]

    def flaws(self):
        return [f for f in self.properties if isinstance(f, Asset.Flaw)]

    def validate(self, new_char):
        if new_char:
            if sum([f.cost() for f in self.features()]) < 2:
                return self.err("Assets created at chargen should have at least two features.")
            if len(self.flaws()) < 1:
                return self.err("Assets created at chargen should have at least one flaw.")
        else:
            if len(self.features()) < 1:
                return self.err("Assets should have a feature.")

        if self.type in [AssetTypes.ALLY, AssetTypes.DEVICE]:
            if self.functional is None:
                return self.err("Allies and Devices must have functional aspects.")
            if self.guiding is not None:
                return self.err("Allies and Devices should not have a guiding aspect.")

        if self.type == AssetTypes.TECH:
            if self.guiding is None:
                return self.err("Techniques must have a guiding aspect.")
            if self.functional is not None and not self.silence_gm:
                return self.err("Techniques should only have functional aspects with gm approval. "
                                "(set gm_approved to silence this warning.)")

        if not self.refresh(check=True):
            return False

        if self.type == AssetTypes.ALLY and not self.has_prop(Asset.Professional):
            return self.err("Allies gain one rank of Professional for free.")
        return all([f.validate() for f in self.properties])

    def render(self, engine):
        engine.subheading(self.name())
        engine.kv("Type", self.type.value)
        if self.functional is not None:
            engine.aspect("Functional Aspect", self.functional)
        if self.guiding is not None:
            engine.aspect("Guiding Aspect", self.guiding)
        engine.kv("Features", ", ".join([f.render(engine) for f in self.features()]))
        engine.kv("Flaws", ", ".join([f.render(engine) for f in self.flaws()]))
        engine.kv("Cost", "{} refresh".format(self.refresh()))
