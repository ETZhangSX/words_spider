from enum import Enum

from orator import Model, scope


class Task(Model):
    __guarded__ = ['id']

    @scope
    def unfinished(self, query):
        return query.where_in('state', [TaskState.INITIAL.value, TaskState.PENDING.value])

    @scope
    def of_spider(self, query, spider):
        return query.where('spider', spider)

    def success(self):
        self.state = TaskState.SUCCESS.value
        self.save()

class TaskState(Enum):
    INITIAL = 0
    SUCCESS = 1
    FAIL = 2
    PENDING = 3 # 已经开始，但还没确认处理成功或失败