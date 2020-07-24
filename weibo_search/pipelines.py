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


class CsvPipeline(object):
    def process_item(self, item, spider):
        base_dir = 'output_files' + os.sep + item['keyword']
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


class WeiboSearchPipeline:
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):
    # def __init__(self):
    #
    #     # # self.ids_seen = set()

    def process_item(self, item, spider):
        # settings = get_project_settings()
        # keyword_list = settings.get('KEYWORD_LIST')

        # for kw in keyword_list:
        #     for file in os.listdir('output_files/%s' % kw):
        #         if file.find(item['weibo']['id']):
        #             raise DropItem("Filter Repetitive Weibo: %s" % item)
        #         break
        # else:
        #     return item
        id_file = 'output_files/weibo_ids.txt'
        # if not os.path.exists(id_file):

        with open(id_file) as f:
            ids_seen = f.read().splitlines()
        if item['weibo']['id'] in ids_seen:
            raise DropItem("Filter Repetitive Weibo: %s" % item)
        else:
            # self.ids_seen.append(item['weibo']['id'])
            with open(id_file, 'a') as f:
                f.write('%s\n' % item['weibo']['id'])
                # self.ids_seen = f.read().splitlines()
            return item