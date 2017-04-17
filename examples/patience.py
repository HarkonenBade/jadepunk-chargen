# -*- coding: UTF-8 -*-

from jadepunk import Character, Aspects, Attrs, Asset, AssetTypes, AttrTypes
import engine

patience = Character("Patience Boyd",
                     aspects=Aspects(portrayal='Gunslinger for Justice',
                                     background="The Enforcer's Daughter",
                                     inciting_incident="The Watch Crippled The Only Good Person I Know",
                                     belief="(Only) the virtuous deserve obedience",
                                     trouble="Just Couldn't Let It Lie"),
                     attrs=Attrs(aristocrat=1,
                                 engineer=1,
                                 explorer=2,
                                 fighter=2,
                                 scholar=0,
                                 scoundrel=3),
                     assets=[Asset(AssetTypes.DEVICE,
                                   name="The Compelling Arguments",
                                   functional="My Mother's Red Jade Revolvers",
                                   features=[Asset.Harmful(3),
                                             Asset.Numerous(1)],
                                   flaws=[Asset.Demanding(1, AttrTypes.FIGHTER)]),
                             Asset(AssetTypes.ALLY,
                                   name="Father Michael Boyd",
                                   functional="Priest to the shunned",
                                   features=[Asset.Professional(2,
                                                                avg=AttrTypes.SCHOLAR,
                                                                fair=AttrTypes.ARISTOCRAT),
                                             Asset.Focus(AttrTypes.SCHOLAR)],
                                   flaws=[Asset.Limited(1)]),
                             Asset(AssetTypes.TECH,
                                   name="All The Best Insults",
                                   features=[Asset.Flexible(AttrTypes.SCOUNDREL, AttrTypes.ARISTOCRAT)],
                                   flaws=[Asset.Situational("Only when making people angry")])])

patience.render(engine.Markdown)
