# -*- coding: utf-8 -*-
from datetime import datetime

__author__ = 'liying'


class DataInfo(object):
    def __init__(self):
        self.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.manifest_files_num = 0
        self.projects_num = 0
        self.revisions_num = 0

    @staticmethod
    def keys():
        return 'update_time', 'manifest_files_num', 'projects_num', 'revisions_num'

    def __getitem__(self, item):
        return getattr(self, str(item))
