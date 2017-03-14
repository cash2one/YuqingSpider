# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'

import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from alarm import alarm
from hot import hot_event
from topic import topic
from burst import burst_event


define('port', default=8999, help='run on the given port', type=int)


class YuqingWebService:
    def start(self):
        tornado.options.parse_command_line()
        # app = tornado.web.Application(handlers=[(r"/detector/(.*)", AdDetectorHandler)])
        app = tornado.web.Application(handlers=[(r"/yuqing/(.*)", YuqingFunctionHandler)])
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port, address='0.0.0.0')
        tornado.ioloop.IOLoop.instance().start()


class YuqingFunctionHandler(tornado.web.RequestHandler):

    def post(self, api_type):
        data = self.request.body
        input = data.decode("utf-8")
        input = json.loads(input)
        ip = self.request.remote_ip
        # self.write("{\"code\":200,\"msg\":\"ok\"}")
        print api_type
        result = ""
        try:
            if api_type == "topic":
               result = topic(input)
            elif api_type == "hot":
               result = hot_event(input)
            elif api_type == "burst":
               result = burst_event(input)
            elif api_type == "alarm":
               result = alarm(input)
        except Exception, e:
            result = {}
            result['sid'] = ""
            result['reaData'] = ""

        self.write(json.dumps(result))

    def get(self, api_type):
        self.post(api_type)

    def put(self, api_type):
        self.post(api_type)


if __name__ == "__main__":
    test = YuqingWebService()
    test.start()
