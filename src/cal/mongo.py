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
import time
import pymongo
from datetime import datetime

class MongoDB():
    """
    Mainly for batch read-write encapsulation of database, reduce the load of database
    api document: http://api.mongodb.com/python/current/examples/bulk.html
    """

    def __init__(self, host=None,
                 port=None,
                 document_class=dict,
                 tz_aware=None,
                 connect=None,
                 type_registry=None,
                 db=None,
                 collection=None,
                 auth_user=None,
                 auth_password=None,
                 auth_db=None,
                 auth_method="SCRAM-SHA-1",
                 **kwargs):
        try:
            self.client = pymongo.MongoClient(host=host,
                                              port=int(port),
                                              document_class=document_class,
                                              tz_aware=tz_aware,
                                              connect=connect,
                                              type_registry=type_registry,
                                              **kwargs)
            if all([auth_db, auth_user, auth_password]):
                self.auth_db = eval("self.client.%s" % auth_db)
                self.auth_db.authenticate(auth_user, auth_password, mechanism=auth_method)

            self.db = eval("self.client.%s" % db)
            self.collection = eval("self.db.%s" % collection)
        except Exception as e:
            raise Exception("---Connect Error---\
                            \n[ %s ]" % str(e))

    def write(self, data):
        """
        write data to Mongodb
        :param data: [{"a":1},{"b":2}]
        :return: None
        """
        try:
            self.collection.insert(data)
        except Exception as e:
            self.output(str(e))

    def read(self, search_method="find()"):
        """
        read data from Mongodb
        :param search_method:
            1.find()
            2.find().limit(2)
            3.find().skip(2)
            4.find({"a": 1})
            and so on...
        :return: result by search
        """
        try:
            result = eval("self.collection.%s" % search_method)
            return result
        except Exception as e:
            print(str(e))

    def update(self, before, after, **kwargs):
        try:
            self.collection.update(before, after, **kwargs)
        except Exception as e:
            self.output(str(e))

    def collection_operator(self, operation, **kwargs):
        try:
            return eval("self.collection.%s" % operation)
        except Exception as e:
            print(str(e))

    def database_operator(self, operation, **kwargs):
        try:
            return eval("self.db.%s" % operation)
        except Exception as e:
            self.output(str(e))

    def get_collection(self):
        return self.collection

    def get_database(self):
        return self.db

    def __del__(self):
        try:
            self.close()
        except Exception as e:
            pass

    def close(self):
        self.client.close()

    def output(self, arg):
        print(str(arg))


def test_connnect():
    host = "52.82.8.245"
    port = "9099"
    auth_user = "root"
    auth_password = "N2m3a6b9k7x"
    auth_db = "admin"
    db = "lijiacai_test"
    collection = "test"
    mongodb = MongoDB(host=host, port=port, auth_user=auth_user, auth_password=auth_password, auth_db=auth_db, db=db,
                      collection=collection)
    data = [{"1": "1", "2": "2"}, {"3": "3"}]
    # mongodb.write(data=data)
    # print(list(mongodb.read()))
    before = {"1": "1", "2": "2"}
    after = {"1": "31111111111"}
    mongodb.update(before, after)


if __name__ == '__main__':
    test_connnect()
