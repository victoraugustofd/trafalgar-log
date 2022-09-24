from dataclasses import dataclass


@dataclass
class PerformanceSecondInnerDataTest:
    a: object = None
    b: object = None
    c: object = None
    d: object = None
    e: object = None
    f: object = None
    g: object = None
    h: object = None
    i: object = None
    j: object = None
    k: object = None
    l: object = None
    m: object = None
    n: object = None
    o: object = None
    p: object = None
    q: object = None
    r: object = None
    s: object = None
    t: object = None
    u: object = None
    v: object = None
    w: object = None
    x: object = None
    y: object = None
    z: object = None


@dataclass
class PerformanceInnerDataTest:
    z: PerformanceSecondInnerDataTest
    a: object = None
    b: object = None
    c: object = None
    d: object = None
    e: object = None
    f: object = None
    g: object = None
    h: object = None
    i: object = None
    j: object = None
    k: object = None
    l: object = None
    m: object = None
    n: object = None
    o: object = None
    p: object = None
    q: object = None
    r: object = None
    s: object = None
    t: object = None
    u: object = None
    v: object = None
    w: object = None
    x: object = None
    y: object = None


@dataclass
class PerformanceDataTest(object):
    z: PerformanceInnerDataTest
    a: object = None
    b: object = None
    c: object = None
    d: object = None
    e: object = None
    f: object = None
    g: object = None
    h: object = None
    i: object = None
    j: object = None
    k: object = None
    l: object = None
    m: object = None
    n: object = None
    o: object = None
    p: object = None
    q: object = None
    r: object = None
    s: object = None
    t: object = None
    u: object = None
    v: object = None
    w: object = None
    x: object = None
    y: object = None
