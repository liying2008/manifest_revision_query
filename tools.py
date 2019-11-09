# -*- coding: utf-8 -*-
import json
import os
import shutil

from data_info import DataInfo

__author__ = 'liying'

SEPARATOR = '@@'

static_dir = ''
result_manifests_dir = static_dir + '/manifests'
result_projects_dir = static_dir + '/projects'
result_paths_dir = static_dir + '/paths'

data_info = DataInfo()


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
    revision_set = set()
    for project, item_list in projects.items():
        project_list.append(project)
        data_list = []
        for item in item_list:
            data = {}
            data['manifest'] = item.manifest
            data['project'] = project
            data['path'] = item.path
            data['revision'] = item.revision
            revision_set.add(item.revision)
            data_list.append(data)

        file_name = result_projects_dir + '/' + str(project).replace('/', SEPARATOR)
        file_name = file_name.strip()
        with open(file_name, 'w') as fp:
            json.dump(data_list, fp)

    data_info.projects_num = len(project_list)
    with open(static_dir + '/projects.list', 'w') as fp:
        fp.write('\n'.join(project_list))
    with open(static_dir + '/revisions.list', 'w') as fp:
        fp.write('\n'.join(revision_set))


def paths_to_json_file(paths):
    path_list = []
    for path, item_list in paths.items():
        path_list.append(path)
        data_list = []
        for item in item_list:
            data = {}
            data['manifest'] = item.manifest
            data['project'] = item.project
            data['path'] = path
            data['revision'] = item.revision
            data_list.append(data)

        file_name = result_paths_dir + '/' + str(path).replace('/', SEPARATOR)
        file_name = file_name.strip()
        with open(file_name, 'w') as fp:
            json.dump(data_list, fp)

    with open(static_dir + '/paths.list', 'w') as fp:
        fp.write('\n'.join(path_list))


def write_manifest_list_to_file():
    files = os.listdir(result_manifests_dir)
    manifest_file_list = list(map(lambda it: it.replace(SEPARATOR, '/'), files))
    data_info.manifest_files_num = len(manifest_file_list)
    with open(static_dir + '/manifests.list', 'w') as fp:
        fp.write('\n'.join(manifest_file_list))


def check_static_dir(static_dir_path):
    global static_dir
    global result_manifests_dir
    global result_projects_dir
    global result_paths_dir
    static_dir = static_dir_path
    result_manifests_dir = static_dir + '/manifests'
    result_projects_dir = static_dir + '/projects'
    result_paths_dir = static_dir + '/paths'

    if not os.path.exists(static_dir):
        os.makedirs(static_dir, 0o777)
    if os.path.exists(result_manifests_dir):
        shutil.rmtree(result_manifests_dir)
    if os.path.exists(result_projects_dir):
        shutil.rmtree(result_projects_dir)
    if os.path.exists(result_paths_dir):
        shutil.rmtree(result_paths_dir)
    os.mkdir(result_manifests_dir, 0o777)
    os.mkdir(result_projects_dir, 0o777)
    os.mkdir(result_paths_dir, 0o777)


def write_data_info_to_file():
    with open(static_dir + '/data_info.json', 'w') as fp:
        fp.write(json.dumps(dict(data_info)))
