import sys

import yaml

from . import Aspects, AspectTypes, Asset, AssetTypes, Attrs, AttrTypes, Character
from .engine import EngineLoader


def get_prop_class(name):
    return getattr(Asset, name)


def props(args):
    return {k: v for k, v in args.items() if k[0].isupper()}


def non_props(args):
    return {k: v for k, v in args.items() if not k[0].isupper()}


def make_prop(name, args):
    cls = get_prop_class(name)
    if cls == Asset.Talented:
        prop = None
        for key in props(args):
            prop = make_prop(key, args[key])
        return cls(prop=prop, **non_props(args))
    if isinstance(args, dict):
        return cls(**args)
    elif isinstance(args, list):
        return cls(*args)
    else:
        return cls(args)


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
        for key in props(asset):
            prop = make_prop(key, asset[key])
            if isinstance(prop, Asset.Feature):
                features.append(prop)
            else:
                flaws.append(prop)
        char_assets.append(Asset(features=features,
                                 flaws=flaws,
                                 **non_props(asset)))
    char_params = {k: v for k, v in char_data.items() if k not in ['aspects', 'attrs', 'assets']}
    Character(aspects=char_aspects,
              attrs=char_attrs,
              assets=char_assets,
              **char_params).render(engine)


if __name__ == "__main__":
    if sys.argv[1] in ["yml", "yaml"]:
        from_yaml(sys.argv[2], EngineLoader(sys.argv[3]))
