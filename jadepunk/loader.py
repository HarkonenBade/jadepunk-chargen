import sys

import yaml

from . import Aspects, AspectTypes, Asset, AssetTypes, Attrs, AttrTypes, Character

import engine


def from_yaml(yml_path, engine):
    def load_type(enum, tag):
        def load(loader, node):
            return enum[loader.construct_scalar(node)]
        yaml.add_constructor(tag, load)
    load_type(AspectTypes, "!Aspect")
    load_type(AssetTypes, "!Asset")
    load_type(AttrTypes, "!Attr")

    with open(yml_path) as yml:
        char_data = yaml.load(yml)

    char_aspects = Aspects(**char_data['aspects'])
    char_attrs = Attrs(**char_data['attrs'])
    char_assets = []
    for asset in char_data['assets']:
        features = []
        flaws = []
        for key in asset:
            if key[0].isupper():
                cls = getattr(Asset, key)
                if isinstance(asset[key], dict):
                    obj = cls(**asset[key])
                else:
                    obj = cls(asset[key])
                if issubclass(cls, Asset.Feature):
                    features.append(obj)
                else:
                    flaws.append(obj)
        params = {k: v for k, v in asset.items() if not k[0].isupper()}
        char_assets.append(Asset(features=features,
                                 flaws=flaws,
                                 **params))
    char_params = {k: v for k, v in char_data.items() if k not in ['aspects', 'attrs', 'assets']}
    Character(aspects=char_aspects,
              attrs=char_attrs,
              assets=char_assets,
              **char_params).render(engine)


if __name__ == "__main__":
    if sys.argv[1] in ["yml", "yaml"]:
        if sys.argv[3] == "moinmoin":
            from_yaml(sys.argv[2], engine.MoinMoin)
        elif sys.argv[3] == "markdown":
            from_yaml(sys.argv[2], engine.Markdown)