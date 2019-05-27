# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html


import json
from scrapy.exceptions import IgnoreRequest
import traceback

from words.models.fail import Fail, FailState
from words.models.task import Task, TaskState

# 记录任务，如果有异常返回，记录任务出错信息
class TaskDownloaderMiddleware(object):

    def process_request(self, request, spider):
        # 1. 寻找有没有匹配的任务，如果没有，利用相关信息创建一个
        task_id = request.meta.get('task_id')
        # 如果没有显式用 item 定义任务，就自动创建一个
        if task_id is None:
            # 根据 url 检测有没有相同的任务
            task = Task.where('url', '=', request.url).first()
        else:
            task = Task.find(task_id)

        if task is None:
            task = Task()
            task.spider = spider.name
            task.callback = 'parse' if request.callback is None else request.callback.__name__
            task.url = request.url
            task.state = TaskState.PENDING.value
            # 如何描述此任务? 如何在 meta 中记录有用的信息?
            task.keyword1 = request.meta.get('keyword1')
            task.keyword2 = request.meta.get('keyword2')
        else:
            # TODO: 以后这里处理何种情况下需要忽略任务
            task.state = TaskState.PENDING.value

        # crawl spider's meta data
        rule = request.meta.get('rule')
        link_text = request.meta.get('link_text')
        if rule or link_text:
            task.meta = json.dumps({
                'rule': rule,
                'link_text': link_text
            })
        task.save()

        request.meta['task_id'] = task.id
        request.meta['task'] = task

    def process_response(self, request, response, spider):
        status_code = response.status
        if status_code not in [200]:
            meta = request.meta
            task_id = meta['task_id']
            fail = Fail.init_fail(task_id)
            fail.state = FailState.UNEXPECTED_STATUS_CODE.value
            fail.errmsg = '异常返回状态码: %d' % status_code
            fail.save()
            raise IgnoreRequest
        else:
            return response

    def process_exception(self, request, exception, spider):
        try:
            if not isinstance(exception, IgnoreRequest):
                meta = request.meta
                task_id = meta['task_id']
                fail = Fail.init_fail(task_id)
                fail.state = FailState.ERROR.value
                fail.errmsg = traceback.format_exception_only(type(exception), exception)
                fail.save()
        except:
            traceback.print_exc()


class TaskSpiderMiddleware(object):

    def process_spider_output(self, response, result, spider):
        task = response.meta['task']
        task.success()
        return result

    def process_spider_exception(self, response, exception, spider):
        task_id = response.meta['task_id']
        fail = Fail.init_fail(task_id)
        fail.state = FailState.ERROR.value
        fail.errmsg = fail.errmsg = traceback.format_exception_only(type(exception), exception)
        fail.save()