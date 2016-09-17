#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wtq'

from pymongo import MongoClient

from config import MONGODB_HOST, MONGODB_PORT


def client_mongo(mongo_host=MONGODB_HOST, mongo_port=MONGODB_PORT):
    """

    :param mongo_host:
    :param mongo_port:
    :return:
    """
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    return client
