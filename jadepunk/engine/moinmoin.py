from . import EngineLoader
from .base import BaseEngine


@EngineLoader.register("moinmoin")
class MoinMoin(BaseEngine):
    BOLD_EM = 3
    ITAL_EM = 2
    TITLE_HEADER = 2
    KV_END = "\n\n"

    @classmethod
    def header(cls, txt, lv):
        cls.text("{l} {t} {l}".format(t=txt, l="="*lv))

    @classmethod
    def em(cls, txt, num):
        return "{l}{t}{l}".format(t=txt, l="'"*num)
