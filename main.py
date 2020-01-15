# !/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json
import time

from baidu import Index
from save import Baidu
from src_data import *

index = Index()


def main():
    err = []
    for date in dates:
        range_date = get_range_date(date)
        for parent, words in all_words.items():
            for area_id, area_name in all_areas.items():
                for word in words:
                    if word in nothing:
                        continue
                    try:
                        print(
                            f'fetch {parent},{word},{area_name},{date}')
                        data = index.index(
                            word, area_id, range_date[0], range_date[1])

                        index_type = data['userIndexes'][0]['type']
                        index_all = json.dumps(data['userIndexes'][0]['all'])
                        index_pc = json.dumps(data['userIndexes'][0]['pc'])
                        index_wise = json.dumps(data['userIndexes'][0]['wise'])
                        ratio_all = json.dumps(data['generalRatio'][0]['all'])
                        ratio_pc = json.dumps(data['generalRatio'][0]['pc'])
                        ratio_wise = json.dumps(data['generalRatio'][0]['wise'])

                        b = Baidu(
                            area=area_name,
                            parent=parent,
                            word=word,
                            index_type=index_type,
                            index_all=index_all,
                            index_pc=index_pc,
                            index_wise=index_wise,
                            ratio_all=ratio_all,
                            ratio_pc=ratio_pc,
                            ratio_wise=ratio_wise,
                            range_date=date,
                        )
                        b.Create()
                        time.sleep(3)
                    except:
                        err.append([parent, word, area_id, date])
                        pass

    print(err)


def retry():
    err = []
    for r in retry_data:
        parent, word, area_id, date = r
        range_date = get_range_date(date)
        area_name = all_areas[area_id]
        try:

            print(f'fetch {parent},{word},{area_name},{date}')

            data = index.index(word, area_id, range_date[0], range_date[1])
            index_type = data['userIndexes'][0]['type']
            index_all = json.dumps(data['userIndexes'][0]['all'])
            index_pc = json.dumps(data['userIndexes'][0]['pc'])
            index_wise = json.dumps(data['userIndexes'][0]['wise'])
            ratio_all = json.dumps(data['generalRatio'][0]['all'])
            ratio_pc = json.dumps(data['generalRatio'][0]['pc'])
            ratio_wise = json.dumps(
                data['generalRatio'][0]['wise'])

            b = Baidu(
                area=area_name,
                parent=parent,
                word=word,
                index_type=index_type,
                index_all=index_all,
                index_pc=index_pc,
                index_wise=index_wise,
                ratio_all=ratio_all,
                ratio_pc=ratio_pc,
                ratio_wise=ratio_wise,
                range_date=date,
            )
            b.Create()
            time.sleep(3)
        except:
            err.append([parent, word, area_id, date])
    print(err)


if __name__ == '__main__':
    retry()
