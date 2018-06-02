# -*- coding: utf-8 -*-

from search import SearchEngine

engine = SearchEngine()

engine.add("1", "菊花残满地伤")
engine.add("2", "桂花菊花桃花")
engine.add("3", "菊花菊花菊花")
engine.add("4", "菊花菊花")

r1 = engine.search("菊花")
for r in r1:
    print(r.decode('utf-8'))

r2= engine.search("桃花")
for r in r2:
    print(r.decode("utf-8"))
