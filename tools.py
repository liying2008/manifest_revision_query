# -*- coding: utf-8 -*-
import json
import os
import shutil

__author__ = 'liying'

SEPARATOR = '@@'

result_dir = 'frontend/static'
result_manifests_dir = result_dir + '/manifests'
result_projects_dir = result_dir + '/projects'


def dict_to_json_file(manifest_file, item_dict):
    data_list = []
    for project, item in item_dict.items():
        # 真实的 project 为 @@ 之前的名称
        project = project.split(SEPARATOR)[0]
        data = {}
        data['manifest'] = manifest_file
        data['project'] = project
        data['path'] = item.path
        data['revision'] = item.revision
        data_list.append(data)
    file_name = result_manifests_dir + '/' + str(manifest_file).replace('/', SEPARATOR)
    file_name = file_name.strip()
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
        file_name = file_name.strip()
        with open(file_name, 'w') as fp:
            json.dump(data_list, fp)

    with open(result_dir + '/projects.list', 'w') as fp:
        fp.write('\n'.join(project_list))


def write_manifest_list_to_file(manifest_file_list):
    with open(result_dir + '/manifests.list', 'w') as fp:
        fp.write('\n'.join(manifest_file_list))


def check_result_dir():
    if os.path.exists(result_manifests_dir):
        shutil.rmtree(result_manifests_dir)
    if os.path.exists(result_projects_dir):
        shutil.rmtree(result_projects_dir)
    os.mkdir(result_manifests_dir, mode=0o777)
    os.mkdir(result_projects_dir, mode=0o777)
