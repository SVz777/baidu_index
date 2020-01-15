import json

from save import Baidu


def s2i(s):
    try:
        return int(s)
    except ValueError:
        return 0


def cal_sum(b: Baidu):
    if b.index_type != 'day':
        raise Exception('err', b.index_type)

    index_all = json.loads(b.index_all)
    return b.area, sum([s2i(i)
                        for i in index_all['data'].split(',')])