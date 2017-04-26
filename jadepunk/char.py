from .validation import Validator


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
        val = Validator(new_gen)
        self.validate(val)
        val.check()

    def refresh(self):
        return self.max_ref - sum([asset.refresh() for asset in self.assets])

    def validate(self, val):
        if self.name == "":
            val.err("Character must have a name.")

        self.aspects.validate(val)
        self.attrs.validate(val)
        for asset in self.assets:
            asset.validate(val)

        if val.new_char and self.max_ref != 7:
            val.err("Starting chars have 7 refresh max")
        if self.refresh() <= 1:
            val.err("Char cannot have 0 or negative refresh")

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
