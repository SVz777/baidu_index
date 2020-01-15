import json
import time

from save import Baidu
from baidu import Index
from src_data import *
from utils import s2i, cal_sum
from typing import List

Baidus = List[Baidu]


def get_data() -> Baidus:
    base_datas = Baidu.Fetch([
        [
            ['id', '>=', 1687],
            ['index_all', 'like', '%"data": ""%'],
        ]
    ],
        None,
        None,
        -1,
        ['id', 'parent', 'word', 'area', 'range_date'])

    ret_datas = []
    temp_num = {}
    for data in base_datas:
        if data.word not in temp_num:
            sum = 0
            ll: Baidus = Baidu.Fetch([[
                ['word', '=', data.word],
                ['range_date', '=', data.range_date]
            ]],
                None,
                None,
                100,
                ['area', 'index_type', 'index_all'])
            for i in ll:
                _, num = cal_sum(i)
                sum += num
            temp_num[data.word] = sum

        elif temp_num[data.word] != 0:
            ret_datas.append(data)

    return ret_datas


if __name__ == '__main__':
    datas = get_data()
    index = Index()
    err = []
    for data in datas:
        try:
            range_date = get_range_date(data.range_date)
            print(f'fetch {data.id} {data.parent},{data.word},{data.area},{data.range_date}')
            ret_data = index.index(
                data.word, areas_flip[data.area], range_date[0], range_date[1])
            if ret_data['userIndexes'][0]['all']['data'] != '':
                print('data update')
                data.index_type = ret_data['userIndexes'][0]['type']
                data.index_all = json.dumps(ret_data['userIndexes'][0]['all'])
                data.index_pc = json.dumps(ret_data['userIndexes'][0]['pc'])
                data.index_wise = json.dumps(ret_data['userIndexes'][0]['wise'])
                data.ratio_all = json.dumps(ret_data['generalRatio'][0]['all'])
                data.ratio_pc = json.dumps(ret_data['generalRatio'][0]['pc'])
                data.ratio_wise = json.dumps(ret_data['generalRatio'][0]['wise'])
                data.Update()
        except Exception as e:
            err.append(data.id)
            print(e)

        time.sleep(3)
    print(err)