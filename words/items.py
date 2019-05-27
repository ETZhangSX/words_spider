# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from datetime import datetime

from scrapy import Field, Item
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

def strip(s):
    return s.strip()


def parse_datetime1(d):
    return datetime.strptime(d, '%Y-%m-%d %H:%M:%S')


def parse_datetime2(d):
    return datetime.strptime(d, '%Y年%m月%d日 %H:%M:%S')


def parse_datetime(d):
    try:
        return parse_datetime1(d)
    except:
        return parse_datetime2(d)


def to_int(s):
    return int(s)


class TaskItem(Item):
    spider = Field(output_processor=TakeFirst())
    callback = Field(output_processor=TakeFirst())
    url = Field(input_processor=MapCompose(strip), output_processor=TakeFirst())
    keyword1 = Field(input_processor=MapCompose(strip), output_processor=TakeFirst())
    keyword2 = Field(input_processor=MapCompose(strip), output_processor=TakeFirst())
    # meta 可直接用 json
    meta = Field()
    tags = Field(input_processor=MapCompose(remove_tags, strip), output_processor=Join(separator=','))
    target_created_at = Field(input_processor=MapCompose(remove_tags, parse_datetime), output_processor=TakeFirst())
    target_updated_at = Field(input_processor=MapCompose(remove_tags, parse_datetime), output_processor=TakeFirst())


class ArticleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    task_id = Field(output_processor=TakeFirst())
    source = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    author = Field(output_processor=TakeFirst())
    tags = Field(input_processor=MapCompose(remove_tags, strip), output_processor=Join(separator=','))
    content = Field(output_processor=TakeFirst())
    view_count = Field(input_processor=MapCompose(to_int), output_processor=TakeFirst())
    comment_count = Field(input_processor=MapCompose(to_int), output_processor=TakeFirst())
    target_created_at = Field(input_processor=MapCompose(remove_tags, parse_datetime2), output_processor=TakeFirst())
    pass

class ImageItem(Item):
    image_urls = Field()
    images = Field()
    article_id = Field()