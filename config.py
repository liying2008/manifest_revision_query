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
        # 需要被排除的 manifest 文件列表
        self.excluded_files = []
        # 忽略并跳过解析错误
        self.ignore_parse_error = False
        # 是否优先解析 upstream 属性
        # True: 先解析 upstream, 无值，再解析 revision
        # False: 只解析 revision
        self.analysis_upstream_first = True
        # 前端static目录（解析结果的存储目录）
        self.frontend_static_dir = 'frontend/static'
