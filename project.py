# -*- coding: utf-8 -*-
import tools

__author__ = 'liying'


class ProjectItem(object):
    def __init__(self):
        self.manifest = ''
        self.path = ''
        self.revision = ''


class PathItem(object):
    def __init__(self):
        self.manifest = ''
        self.project = ''
        self.revision = ''


class Project(object):
    def __init__(self):
        self.projects = {}
        self.paths = {}

    def add_manifest_and_dict(self, manifest_file, item_dict):
        for project, item in item_dict.items():
            # 真实的 project 为 @@ 之前的名称
            project = project.split(tools.PROJECT_DUPLICATION_TAG)[0]
            path = item.path
            revision = item.revision
            # 添加到 projects 字典
            if project not in self.projects:
                self.projects[project] = []
            project_item = ProjectItem()
            project_item.manifest = manifest_file
            project_item.path = path
            project_item.revision = revision
            self.projects[project].append(project_item)
            # 添加到 paths 字典
            if path not in self.paths:
                self.paths[path] = []
            path_item = PathItem()
            path_item.manifest = manifest_file
            path_item.project = project
            path_item.revision = revision
            self.paths[path].append(path_item)
