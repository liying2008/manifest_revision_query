# -*- coding: utf-8 -*-
from xml.dom import minidom

__author__ = 'liying'


class Item(object):
    def __init__(self):
        self.path = ''
        self.revision = ''


class Manifest(object):
    def __init__(self, manifest_file, remote=None, default=None):
        # print("manifest_file", manifest_file)
        # print("remote", remote)
        # print("default", default)
        if remote is None:
            remote = {}
        if default is None:
            default = {}
        self.manifest_file = manifest_file
        self.remote = remote
        self.default = default
        self.items = {}

    def parse_remote(self, remote_tag):
        if remote_tag.hasAttribute('revision'):
            remote_name = remote_tag.getAttribute('name')
            remote_revision = remote_tag.getAttribute('revision')
            self.remote[remote_name] = {}
            self.remote[remote_name]['revision'] = remote_revision

    def parse_default(self, default_tag):
        if default_tag.hasAttribute('revision'):
            self.default['revision'] = default_tag.getAttribute('revision')
        if default_tag.hasAttribute('remote'):
            self.default['remote'] = default_tag.getAttribute('remote')

    def parse_project(self, project_tag):
        item = Item()
        project = project_tag.getAttribute('name')
        if project_tag.hasAttribute('path'):
            item.path = project_tag.getAttribute('path')
        else:
            item.path = project

        if project_tag.hasAttribute('revision'):
            item.revision = project_tag.getAttribute('revision')
        elif project_tag.hasAttribute('remote'):
            remote = project_tag.getAttribute('remote')
            if remote in self.remote:
                item.revision = self.remote[remote]['revision']
            else:
                item.revision = self.default['revision']
        else:
            item.revision = self.default['revision']
        self.items[project] = item

    def parse_include(self, include_tag):
        manifest_name = include_tag.getAttribute('name')
        manifest = Manifest(manifest_name, remote=self.remote, default=self.default)
        items = manifest.parse()
        self.items = dict(self.items, **items)

    def parse_remove_project(self, remove_project_tag):
        name = remove_project_tag.getAttribute('name')
        del self.items[name]

    def parse(self):
        print(self.manifest_file)
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
            print(project + '--' + item.path + '--' + item.revision)
        return self.items
