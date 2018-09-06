# -*- coding: utf-8 -*-
import json
import os

__author__ = 'liying'

SEPARATOR = '@@'

result_dir = 'frontend/static'
result_manifests_dir = result_dir + '/manifests'
result_projects_dir = result_dir + '/projects'


def dict_to_json_file(manifest_file, item_dict):
    data_list = []
    for project, item in item_dict.items():
        data = {}
        data['manifest'] = manifest_file
        data['project'] = project
        data['path'] = item.path
        data['revision'] = item.revision
        data_list.append(data)
    file_name = result_manifests_dir + '/' + str(manifest_file).replace('/', SEPARATOR)
    with open(file_name, 'w') as fp:
        json.dump(data_list, fp)


def projects_to_json_file(projects):
    project_list = []
    for project, item_list in projects.items():
        project_list.append(project)
        data_list = []
        for item in item_list:
            data = {}
            data['manifest'] = item.manifest
            data['project'] = project
            data['path'] = item.path
            data['revision'] = item.revision
            data_list.append(data)

        file_name = result_projects_dir + '/' + str(project).replace('/', SEPARATOR)
        with open(file_name, 'w') as fp:
            json.dump(data_list, fp)

    with open(result_dir + '/projects.list', 'w') as fp:
        fp.write('\n'.join(project_list))


def write_manifest_list_to_file(manifest_file_list):
    with open(result_dir + '/manifests.list', 'w') as fp:
        fp.write('\n'.join(manifest_file_list))


def check_result_dir():
    os.makedirs(result_manifests_dir, exist_ok=True)
    os.makedirs(result_projects_dir, exist_ok=True)
