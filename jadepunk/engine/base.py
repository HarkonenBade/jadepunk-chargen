class EngineLoader(object):
    engine_store = {}

    def __new__(cls, name):
        return cls.engine_store[name]

    @classmethod
    def register(cls, name):
        def wrapper(obj):
            cls.engine_store[name] = obj
            return obj
        return wrapper


class BaseEngine(object):
    BOLD_EM = 0
    ITAL_EM = 0
    TITLE_HEADER = 1
    KV_END = "\n"

    @classmethod
    def header(cls, txt, lv):
        raise NotImplementedError()

    @classmethod
    def em(cls, txt, num):
        raise NotImplementedError()

    @classmethod
    def bold(cls, txt):
        return cls.em(txt, cls.BOLD_EM)

    @classmethod
    def italics(cls, txt):
        return cls.em(txt, cls.ITAL_EM)

    @classmethod
    def boldit(cls, txt):
        return cls.em(txt, cls.ITAL_EM + cls.BOLD_EM)

    @classmethod
    def title(cls, txt):
        cls.header(txt, cls.TITLE_HEADER)

    @classmethod
    def heading(cls, txt):
        cls.header(txt, cls.TITLE_HEADER + 1)

    @classmethod
    def subheading(cls, txt):
        cls.header(txt, cls.TITLE_HEADER + 2)

    @classmethod
    def text(cls, txt, end="\n"):
        print(txt, end=end)

    @classmethod
    def tag(cls, txt):
        cls.text(cls.bold(txt + ":") + " ", end="")

    @classmethod
    def kv(cls, key, value):
        cls.tag(key)
        cls.text(value, end=cls.KV_END)

    @classmethod
    def aspect(cls, key, txt):
        cls.kv(key, cls.boldit(txt))
