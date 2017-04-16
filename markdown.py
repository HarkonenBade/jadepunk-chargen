# -*- coding: UTF-8 -*-

import contextlib

def _header(txt, lv):
    print("{l} {t}".format(t=txt, l="#"*lv))


def _em(txt, num):
    return "{l}{t}{l}".format(t=txt, l="*"*num)

def bold(txt):
    return _em(txt, 2)


def italics(txt):
    return _em(txt, 1)


def boldit(txt):
    return _em(txt, 3)


def title(txt):
    _header(txt, 1)


def heading(txt):
    _header(txt, 2)


def subheading(txt):
    _header(txt, 3)


@contextlib.contextmanager
def section():
    yield


def hline():
    print("***")


def tag(txt):
    print(bold(txt + ":") + " ", end="")


def kv(key, value):
    print("{} {}  ".format(bold(key + ":"), value))


def aspect(key, txt):
    kv(key, boldit(txt))
