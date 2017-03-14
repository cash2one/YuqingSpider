# -*- coding: utf-8 -*-
__author__ = 'wtq'

import time


def test1(i):
    print i
    time.sleep(2)


def delay():
    print 'in delay'
    time.sleep(2)


def test2():
    print 'test2'
    time.sleep(3)


def test_yield():
    for i in range(10):
        yield test1(i)


if __name__ == "__main__":
    a = test_yield()
    for i in a:
        print i

