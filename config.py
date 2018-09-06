# -*- coding: utf-8 -*-


__author__ = 'liying'


class Config(object):
    def __init__(self):
        # manifests 文件所在目录
        self.manifest_root_dir = "manifests"
        # 需要被查询的目录
        self.manifest_dirs_for_query = []
        # 需要被查询的 manifest 文件列表
        self.manifest_file_list = []
