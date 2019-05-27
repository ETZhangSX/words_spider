from orator import Schema

from words.models import db


schema = Schema(db)

schema.drop_if_exists('tasks')
with schema.create('tasks') as table:
    table.increments('id')
    table.string('spider')  # 创建任务的爬虫
    table.string('callback')  # 爬虫回调函数
    table.string('url')  # 请求 url
    table.string('keyword1').nullable()  # 关键词1: 一般是资讯的作者
    table.string('keyword2').nullable()  # 关键词2: 一般是文章的标题
    table.json('meta').nullable()  # 请求元信息
    table.text('tags').nullable()  # 标签，可附加到获取的内容中
    table.integer('state').default(0)  # 状态，表示任务是否需要继续
    table.datetime('target_created_at').nullable()  # 目标创建时间
    table.datetime('target_updated_at').nullable()  # 目标更新时间，用来判断是否需要更新内容
    table.timestamps()

    table.index(['url'])
    table.index(['spider', 'keyword1', 'keyword2'])

    table.index(['spider', 'created_at'])

schema.drop_if_exists('fails')
with schema.create('fails') as table:
    table.increments('id')
    table.integer('task_id').unsigned().unique()
    table.integer('state').default(0)  # 状态，这里的状态是指出错后处理的状态
    table.integer('tries').unsigned()  # 尝试次数（含第一次尝试)
    table.text('errmsg')  # 出错信息，用来修复 bug
    table.timestamps()
    table.index('updated_at')

schema.drop_if_exists('articles')
with schema.create('articles') as table:
    table.increments('id')
    table.integer('task_id').unsigned().unique().nullable()
    table.string('source')
    table.string('url').unique()
    table.string('title')
    table.string('author').nullable()
    table.string('tags').nullable()
    table.long_text('content').nullable()
    table.integer('view_count').nullable()
    table.integer('comment_count').nullable()
    table.datetime('target_created_at').nullable()
    table.datetime('target_updated_at').nullable()
    table.timestamps()

    table.index('task_id')
    table.index('url')
    table.index('title')
    table.index('target_updated_at')
    table.index('updated_at')

