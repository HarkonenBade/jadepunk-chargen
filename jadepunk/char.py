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
