# !/usr/local/bin/python3
# -*- coding: utf-8 -*-
from src_data import *
from save import Baidu
import logging

from utils import cal_sum

logger = logging.getLogger('sakura')
logger.setLevel(logging.WARNING)


def proc_all(res_date_word, bs):
    for b in bs:
        area, all = cal_sum(b)
        res_date_word[area] = all


def initRes():
    res = {}
    for date in done_dates:
        res[date] = {}
        for parent, words in done_all_words.items():
            for word in words:
                if word in nothing:
                    continue
                res[date][word] = {}
                for city_id, city_name in all_areas.items():
                    res[date][word][city_name] = 0

    return res


def analyze():
    wds = []
    res = initRes()
    for date in done_dates:
        for parent, words in done_all_words.items():
            for word in words:
                if word in nothing:
                    continue
                wds.append(word)
                m = Baidu.Fetch([[
                    ['word', '=', word],
                    ['range_date', '=', date],
                ]])
                print(date, word)
                proc_all(res[date][word], m)

    return res


def write2csv(res):
    with open('xxlw.csv', 'w+', encoding='GBK') as file:
        for date, data in res.items():
            print(f'{date}年', ','.join(list(all_areas.values())), sep=',', file=file)

            for word, areas in data.items():
                print(word, ','.join([str(i) for i in areas.values()]), sep=',', file=file)
                if word == '众筹':
                    print('网上投资', ','.join(['' for i in range(32)]), sep=',', file=file)
                elif word == '区块链':
                    print('监管沙盒', ','.join(['' for i in range(32)]), sep=',', file=file)
                    print('金融稳定', ','.join(['' for i in range(32)]), sep=',', file=file)
                elif word == '金融风险':
                    print('监管科技', ','.join(['' for i in range(32)]), sep=',', file=file)
            print(file=file)


if __name__ == '__main__':
    rrr = analyze()
    write2csv(rrr)
