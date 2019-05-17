#!/usr/bin/python
# coding:utf-8

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@Baidu.com.xxxxxx
===========================================
"""

import os
import sys
import json

import matplotlib
matplotlib.use('Agg')

import pandas as  pd
import matplotlib.pyplot as plt
from datetime import datetime
from src.cal.mongo import MongoDB

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass


class MongoQuery():
    def __init__(self, start_time, end_time,collection="carno"):
        """

        :param start_time: 2019_05_17_00_00_00
        :param end_time:
        """
        self.start_time = start_time.split("_")
        self.end_time = end_time.split("_")
        self.st = "%s-%s-%s %s:%s:%s" % (
            self.start_time[0], self.start_time[1], self.start_time[2], self.start_time[3], self.start_time[4],
            self.start_time[5])
        self.et = "%s-%s-%s %s:%s:%s" % (
            self.end_time[0], self.end_time[1], self.end_time[2], self.end_time[3], self.end_time[4], self.end_time[5])
        host = "52.82.8.245"
        port = "9099"
        auth_user = "root"
        auth_password = "N2m3a6b9k7x"
        auth_db = "admin"
        db = "scrapy"
        collection = collection
        mongodb = MongoDB(host=host, port=port, auth_user=auth_user, auth_password=auth_password, auth_db=auth_db,
                          db=db,
                          collection=collection)
        query = 'find({"ts": {"$gte": datetime(%s, %s, %s, %d, %d, %d)}})' % (
            self.start_time[0], self.start_time[1], self.start_time[2], int(self.start_time[3]), int(self.start_time[4]),
            int(self.start_time[5]))
        self.li = mongodb.read(query)
        self.df = pd.DataFrame(list(self.li))
        mongodb.close()

    def filterd(self, appid, station_id=None):
        """
        :param appid: str app名称
        :param station_id: str or None 站点id
        :return: DataFrame
        """
        st = self.st
        et = self.et
        df = self.df.loc[self.df.appid == appid]
        df = df.loc[(df.ts >= st) & (df.ts < et)]
        assert df.empty is False
        if station_id:
            return df.loc[df.station_id == station_id]
        else:
            return df

    def get_order(self, appid, station_id=None):
        """
        :return: int 订单量
        """
        st = self.st
        et = self.et
        df = self.filterd(appid, station_id)
        df = df.loc[df.status == -1]
        return abs(df.status.sum())

    def get_trend(self, appid, interval, station_id=None, path=None, plot=False):
        """
        :param interval:str 间隔时间 例如1min 1h 1s 1D 24h
        :param path: str or None保存图片路径
        :param plot: bool 是否作图
        :return: Series or None
        """
        st = self.st
        et = self.et
        df = self.filterd(appid, station_id)
        df = df.set_index('ts')
        s = df.status.map(abs)
        res = s.resample(interval).sum()
        if plot:
            if path:
                res.plot()
                plt.savefig(path)
                return res
            else:
                raise ValueError('path is None')
        else:
            return res

    def Flow(self, appid, station_id=None, freq=True):
        """
        :param station_id: str or None
        :param freq: bool 是否计算频数
        :return: Series
        """
        st = self.st
        et = self.et
        df = self.filterd(appid, station_id)
        try:
            df = df[['carno', 'ts', 'station_id', 'status']]
        except KeyError:
            raise KeyError('carno,ts,station_id status 必须包含这三个字段')
        df = df.sort_values(['carno', 'ts'])
        dfb = df.shift(1)
        dfb.columns = ['carno1', 'ts1', 'station_id1', 'status1']
        dfz = pd.concat([dfb, df], axis=1)
        dfz = dfz.loc[dfz.carno1 == dfz.carno]
        dfz = dfz.loc[(dfz.status1 == -1) & (dfz.status == 1)]
        dfz['lx'] = dfz.station_id1 + '->' + dfz.station_id
        lx = dfz.lx

        if freq:
            return lx.value_counts()
        return lx

    def __del__(self):
        pass


def test():
    start_time = "2019_05_16_00_00_00"
    end_time = "2019_05_17_00_00_00"
    m = MongoQuery(start_time=start_time, end_time=end_time)
    df = m.get_order('长安出行', station_id='93')
    print((df))

if __name__ == '__main__':
    test()
