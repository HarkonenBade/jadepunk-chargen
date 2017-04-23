from . import EngineLoader
from .base import BaseEngine


@EngineLoader.register("markdown")
class Markdown(BaseEngine):
    BOLD_EM = 2
    ITAL_EM = 1
    TITLE_HEADER = 1
    KV_END = "  \n"

    @classmethod
    def header(cls, txt, lv):
        print("{l} {t}".format(t=txt, l="#"*lv))

    @classmethod
    def em(cls, txt, num):
        return "{l}{t}{l}".format(t=txt, l="*"*num)
