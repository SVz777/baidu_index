import json
import time

from tqdm import tqdm

from save import Baidu
from baidu import Index
from src_data import *
from utils import cal_sum
from typing import List

Baidus = List[Baidu]


def get_data() -> Baidus:
    base_datas = Baidu.Fetch([
        [
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
                ['area', '!=', '全国'],
                ['range_date', '=', data.range_date],
            ]],
                None,
                None,
                -1,
                ['area', 'index_type', 'index_all'])
            for i in ll:
                _, num = cal_sum(i)
                sum += num
            temp_num[data.word] = sum

        elif temp_num[data.word] > 100:
            ret_datas.append(data)

    return ret_datas


if __name__ == '__main__':
    datas = get_data()
    index = Index()
    err = []
    with tqdm(total=len(datas)) as process_bar:
        for data in datas:
            try:
                range_date = get_range_date(data.range_date)
                process_bar.set_description(
                    f'fetch {data.id} {data.parent},{data.word},{data.area},{data.range_date}')
                ret_data = index.index(
                    data.word, areas_flip[data.area], range_date[0], range_date[1])
                if ret_data['userIndexes'][0]['all']['data'] != '':
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
            process_bar.update(1)
            time.sleep(3)
    print(err)
