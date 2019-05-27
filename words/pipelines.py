# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from words.items import TaskItem, ArticleItem, ImageItem
from words.models.article import Article
from words.models.image import Image
from words.models.task import Task, TaskState

# class WordsSpiderPipeline(object):
#     def process_item(self, item, spider):
#         return item


class PersistItemPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, TaskItem):
            # check if task exists
            # 此任务用的 spider 不是创建任务的  spider
            url = item['url']
            # 通过 url 查看有没有相同的任务
            task = Task.where('url', '=', url).first()
            if task is None:
                task = Task()
                task.meta = {}
            else:
                task.meta = json.loads(task.meta)
            task.spider = item['spider']
            task.callback = item['callback']
            task.url = url
            task.keyword1 = item['keyword1']
            task.keyword2 = item['keyword2']
            task.state = TaskState.INITIAL.value
            task.meta = {**task.meta, **item['meta']}
            task.meta = json.dumps(task.meta)
            task.target_created_at = item['target_created_at']
            task.target_updated_at = item['target_updated_at']
            task.save()

        elif isinstance(item, ArticleItem):
            article = Article.first_or_new_by_url(item['url'])
            article.task_id = item['task_id']
            article.source = item['source']
            article.url = item['url']
            article.title = item['title']
            article.author = item['author']
            article.tags = item.get('tags')
            article.content = item['content']
            article.view_count = item['view_count']
            article.comment_count = item['comment_count']
            article.target_created_at = item['target_created_at']
            article.target_updated_at = item['target_updated_at']
            article.save()

        elif isinstance(item, ImageItem):
            self.process_image_item(item, spider)

        return item

    def process_image_item(self, item, spider):
        article_id = item["article_id"]
        images = item["images"]
        for image in images:
            img = Image.find_or_create_by_artile_id_and_url(article_id, image["url"])
            img.path = image["path"]
            img.save()
        Article.where('id', article_id).update(images_num = len(images))
