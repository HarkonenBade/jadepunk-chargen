# -*- coding: UTF-8 -*-

from jadepunk import Character, Aspects, Attrs, Asset, AssetTypes, AttrTypes
import engine

mitsune = Character("Kaneko Mitsune",
                    background="""
Daughter of a councillor, kept like a bird in a cage until one day she decided she had had enough.
""".strip(),
                    aspects=Aspects(portrayal='I am but a "simple musician"',
                                    background="Jewel in their father's crown",
                                    inciting_incident="Trying to leave it all behind",
                                    belief="The corrupt elite only think of themselves",
                                    trouble="Runaway child of a councillor"),
                    attrs=Attrs(aristocrat=3,
                                engineer=0,
                                explorer=1,
                                fighter=2,
                                scholar=2,
                                scoundrel=1),
                    assets=[Asset(AssetTypes.DEVICE,
                                  name="Kashi-dori",
                                  functional="White-Jade Shamisen",
                                  features=[Asset.Focus(AttrTypes.ARISTOCRAT, 2),
                                            Asset.Harmful(1)],
                                  flaws=[Asset.Situational("While being played"),
                                         Asset.Troubling("The prize of a treasury")]),
                            Asset(AssetTypes.TECH,
                                  name="School of the Desert Sirocco",
                                  functional="Student of the Desert Sirocco",
                                  guiding="Jewel in their father's crown",
                                  features=[Asset.Flexible(AttrTypes.FIGHTER,
                                                           AttrTypes.EXPLORER)],
                                  flaws=[Asset.Situational("I need space to perform")],
                                  gm_approved=True)])

mitsune.render(engine.Markdown)
