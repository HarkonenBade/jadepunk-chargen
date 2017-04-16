# -*- coding: UTF-8 -*-

import contextlib

def _header(txt, lv):
    print("{l} {t} {l}".format(t=txt, l="="*lv))


def _em(txt, num):
    return "{l}{t}{l}".format(t=txt, l="'"*num)

def bold(txt):
    return _em(txt, 3)


def italics(txt):
    return _em(txt, 2)


def boldit(txt):
    return _em(txt, 5)


def title(txt):
    _header(txt, 2)


def heading(txt):
    _header(txt, 3)


def subheading(txt):
    _header(txt, 4)


@contextlib.contextmanager
def section():
    yield
    hline()


def hline():
    print("----")


def tag(txt):
    print(bold(txt + ":") + " ", end="")


def kv(key, value):
    print("{} {}\n".format(bold(key + ":"), value))


def aspect(key, txt):
    kv(key, boldit(txt))
