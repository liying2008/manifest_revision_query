# -*- coding: utf-8 -*-
import tools

__author__ = 'liying'


class Item(object):
    def __init__(self):
        self.manifest = ''
        self.path = ''
        self.revision = ''


class Project(object):
    def __init__(self):
        self.projects = {}

    def add_manifest_and_dict(self, manifest_file, item_dict):
        for project, item in item_dict.items():
            # 真实的 project 为 @@ 之前的名称
            project = project.split(tools.SEPARATOR)[0]
            if project not in self.projects:
                self.projects[project] = []
            new_item = Item()
            new_item.manifest = manifest_file
            new_item.path = item.path
            new_item.revision = item.revision
            self.projects[project].append(new_item)
