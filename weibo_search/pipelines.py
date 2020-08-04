# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from config import CRAWLED_PATH

class CsvPipeline(object):
    """Save weibo item into csv files"""
    def process_item(self, item, spider):
        settings = get_project_settings()
        crawl_id = settings.get('CRAWL_ID')
        base_dir = CRAWLED_PATH + '/' + crawl_id + os.sep + item['keyword']
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + item['keyword'] + '.csv'
        if not os.path.isfile(file_path):
            is_first_write = 1
        else:
            is_first_write = 0
        if item:
            with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                if is_first_write:
                    header = [
                        'id', 'bid', 'user_id', '用户昵称', '微博正文', '头条文章url',
                        '发布位置', '艾特用户', '话题', '转发数', '评论数', '点赞数', '发布时间',
                        '发布工具', '微博图片url', '微博视频url', 'retweet_id'
                    ]
                    writer.writerow(header)
                writer.writerow(
                    [item['weibo'][key] for key in item['weibo'].keys()])
        return item


class DuplicatesPipeline(object):
    """Drop duplicate weibo"""
    def process_item(self, item, spider):
        id_file = '%s/weibo_ids.txt' % CRAWLED_PATH

        with open(id_file) as f:
            ids_seen = f.read().splitlines()
        if item['weibo']['id'] in ids_seen:
            raise DropItem("Filter Repetitive Weibo: %s" % item)
        else:
            with open(id_file, 'a') as f:
                f.write('%s\n' % item['weibo']['id'])
                # self.ids_seen = f.read().splitlines()
            return item