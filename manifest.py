# -*- coding: utf-8 -*-
from xml.dom import minidom

import tools

__author__ = 'liying'


class ProjectItem(object):
    def __init__(self):
        self.path = ''
        self.revision = ''


class Manifest(object):
    def __init__(self, manifest_file, remote=None, default=None, analysis_upstream_first=True):
        # print("manifest_file", manifest_file)
        # print("remote", remote)
        # print("default", default)
        if remote is None:
            remote = {}
        if default is None:
            default = {}
        self.analysis_upstream_first = analysis_upstream_first
        self.manifest_file = manifest_file
        self.remote = remote
        self.default = default
        self.items = {}
        self.remove_projects = []
        # 重复的 project
        self.duplicate_projects = {}

    def parse_remote(self, remote_tag):
        remote_name = remote_tag.getAttribute('name')
        if remote_name not in self.remote:
            self.remote[remote_name] = {}
        if remote_tag.hasAttribute('revision'):
            remote_revision = remote_tag.getAttribute('revision')
            self.remote[remote_name]['revision'] = remote_revision
        if remote_tag.hasAttribute('upstream'):
            remote_upstream = remote_tag.getAttribute('upstream')
            self.remote[remote_name]['upstream'] = remote_upstream

    def parse_default(self, default_tag):
        if default_tag.hasAttribute('revision'):
            self.default['revision'] = default_tag.getAttribute('revision')
        if default_tag.hasAttribute('upstream'):
            self.default['upstream'] = default_tag.getAttribute('upstream')
        if default_tag.hasAttribute('remote'):
            self.default['remote'] = default_tag.getAttribute('remote')

    def parse_project(self, project_tag):
        item = ProjectItem()
        project = project_tag.getAttribute('name')
        if project_tag.hasAttribute('path'):
            item.path = project_tag.getAttribute('path')
        else:
            item.path = project
        if self.analysis_upstream_first:
            if project_tag.hasAttribute('upstream'):
                item.revision = project_tag.getAttribute('upstream')
            elif project_tag.hasAttribute('remote'):
                remote = project_tag.getAttribute('remote')
                if remote in self.remote and 'upstream' in self.remote[remote]:
                    item.revision = self.remote[remote]['upstream']
                else:
                    item.revision = self.default.get('upstream', '')
            else:
                item.revision = self.default.get('upstream', '')
        if item.revision == '':
            if project_tag.hasAttribute('revision'):
                item.revision = project_tag.getAttribute('revision')
            elif project_tag.hasAttribute('remote'):
                remote = project_tag.getAttribute('remote')
                if remote in self.remote and 'revision' in self.remote[remote]:
                    item.revision = self.remote[remote]['revision']
                else:
                    item.revision = self.default.get('revision', '')
            else:
                item.revision = self.default.get('revision', '')

        self.add_project(project, item)

    def parse_include(self, include_tag):
        manifest_name = include_tag.getAttribute('name')
        manifest = Manifest(manifest_name, remote=self.remote, default=self.default,
                            analysis_upstream_first=self.analysis_upstream_first)
        items, remote, default, remove_projects = manifest.parse()
        # 1. 处理 remove_projects（必须首先处理）
        for remove_project in remove_projects:
            self.remove_project(remove_project)
        # 2. 处理 items
        for project, item in items.items():
            # 真实的 project 为 @@ 之前的名称
            project = project.split(tools.SEPARATOR)[0]
            self.add_project(project, item)
        # 3. 处理 remote
        self.remote = dict(self.remote, **remote)
        # 4. 处理 default
        self.default = dict(self.default, **default)

    def parse_remove_project(self, remove_project_tag):
        name = remove_project_tag.getAttribute('name')
        self.remove_project(name)

    def add_project(self, project, item):
        if project in self.items:
            # project 之前已存在
            print('[WARNING #1]', project + ' duplicate')
            num = self.duplicate_projects.get(project, 1)
            num += 1
            self.duplicate_projects[project] = num
            self.items[project + tools.SEPARATOR + str(num)] = item
        else:
            self.items[project] = item

    def remove_project(self, project_name):
        if project_name in self.items:
            del self.items[project_name]
        if project_name in self.duplicate_projects:
            num = self.duplicate_projects[project_name]
            for i in range(2, num + 1):
                del self.items[project_name + tools.SEPARATOR + str(i)]
            del self.duplicate_projects[project_name]

    def parse(self):
        """
        解析 manifest 文件
        :return: items
        :return: remote
        :return: default
        :return: remove_projects
        """
        print('[' + self.manifest_file + ']')
        # 解析成 DOM 树
        dom_tree = minidom.parse(self.manifest_file)
        # 得到根节点
        root = dom_tree.documentElement
        # 得到所有子节点
        child_nodes = root.childNodes
        for child_node in child_nodes:
            # 判断是否是元素节点
            if child_node.nodeType == child_node.ELEMENT_NODE:
                node_name = child_node.nodeName
                # print(node_name)
                if node_name == 'remote':
                    self.parse_remote(child_node)
                elif node_name == 'default':
                    self.parse_default(child_node)
                elif node_name == 'project':
                    self.parse_project(child_node)
                elif node_name == 'include':
                    self.parse_include(child_node)
                elif node_name == 'remove-project':
                    self.parse_remove_project(child_node)

        # print(self.remote)
        # print(self.default)
        for project, item in self.items.items():
            print(project + '; ' + item.path + '; ' + item.revision)
        return self.items, self.remote, self.default, self.remove_projects
