# -*- coding: utf-8 -*-
from typing import Iterable

import jieba
from redis import StrictRedis

class SearchEngine(object):

    def __init__(self):
        self.client = StrictRedis()

    def search(self, content):
        # 根据内容查询对应的数据 ID
        names = self.client.zrange(name=content, start=0, end=-1, desc=True)
        result = []
        # 根据 ID 拿数据
        for name in names:
            value = self.client.get(name=name)
            result.append(value)
        return result

    def add(self, name=None, value=""):
        # 存储
        self.client.set(name=name, value=value)
        # 分词
        self.analyze(name, value)
        return True

    # 分词
    def analyze(self, name, value):
        if type(value) == dict:
            for v in value.values():
                analyzed_list = jieba.cut(v, cut_all=False)
                self.generate_analyze_score(name, analyzed_list)
        elif type(value) == str:
            analyzed_list = jieba.cut(value, cut_all=False)
            self.generate_analyze_score(name, analyzed_list)
        elif isinstance(value, Iterable):
            for v in value:
                analyzed_list = jieba.cut(v, cut_all=False)
                self.generate_analyze_score(name, analyzed_list)
        else:
            raise Exception("数据格式错误")

    # 对分词后的结果计算 score
    def generate_analyze_score(self, name, analyzed_list):
        for e in analyzed_list:
            self.client.zincrby(name=e, value=name)
