import enum


class Validator(object):
    class ErrorLevels(enum.Enum):
        WARN = "Warning"
        ERR = "Error"

    def __init__(self, new_char):
        self.val_log = []
        self.new_char = new_char

    def _log(self, lv, txt):
        self.val_log.append((lv, txt))

    def err(self, txt):
        self._log(self.ErrorLevels.ERR, txt)

    def warn(self, txt):
        self._log(self.ErrorLevels.WARN, txt)

    def check(self):
        for lv, txt in self.val_log:
            print("{}: {}".format(lv.value, txt))
        if any([lv == self.ErrorLevels.ERR for lv, txt in self.val_log]):
            print("\n==============INVALID CHAR==============\n")

    def clear(self):
        self.val_log = []
