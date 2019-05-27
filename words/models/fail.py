from enum import Enum

from orator import Model


class Fail(Model):
    __guarded__ = ['id']
    @staticmethod
    def init_fail(task_id):
        fail = Fail.where('task_id', '=', task_id).first()
        if fail is None:
            fail = Fail()
            fail.task_id = task_id
            fail.tries = 1
        else:
            fail.tries += 1
        return fail


class FailState(Enum):
    UNEXPECTED_STATUS_CODE = 1
    ERROR = 2
