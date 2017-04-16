# -*- coding: UTF-8 -*-

from jadepunk import Character, Aspects, Attrs, Asset
import moinmoin

mitsune = Character("Kaneko Mitsune",
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
                    assets=[Asset(Asset.Types.DEVICE,
                                  functional="White-Jade Shamisen",
                                  features=[Asset.Focus(Attrs.Types.ARISTOCRAT),
                                            Asset.Harmful(1)],
                                  flaws=[Asset.Situational("While being played"),
                                         Asset.Troubling("The prize of a treasury")]),
                            Asset(Asset.Types.TECH,
                                  functional="Student of the Desert Sirocco",
                                  guiding="Jewel in their father's crown",
                                  features=[Asset.Flexible(Attrs.Types.FIGHTER,
                                                           Attrs.Types.EXPLORER)],
                                  flaws=[Asset.Situational("I need space to perform")])])

mitsune.render(moinmoin)
