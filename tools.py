# -*- coding: utf-8 -*-
import json
import os
import shutil
from urllib.parse import quote, unquote

from data_info import DataInfo

__author__ = 'liying'

# project 重复的标记
# 同一个manifest中可能存在多个同名project
# 同名project解析时暂时先用@@2、@@3标记一下，之后再处理
PROJECT_DUPLICATION_TAG = '@@'

static_dir = ''
result_manifests_dir = static_dir + '/manifests'
result_projects_dir = static_dir + '/projects'
result_paths_dir = static_dir + '/paths'

data_info = DataInfo()


def dict_to_json_file(manifest_file, item_dict):
    data_list = []
    for project, item in item_dict.items():
        # 真实的 project 为 @@ 之前的名称
        project = project.split(PROJECT_DUPLICATION_TAG)[0]
        data = {
            'manifest': manifest_file,
            'project': project,
            'path': item.path,
            'revision': item.revision
        }
        data_list.append(data)
    file_name = result_manifests_dir + '/' + quote(manifest_file, safe='')
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
            data = {
                'manifest': item.manifest,
                'project': project,
                'path': item.path,
                'revision': item.revision
            }
            revision_set.add(item.revision)
            data_list.append(data)

        file_name = result_projects_dir + '/' + quote(project, safe='')
        file_name = file_name.strip()
        with open(file_name, 'w') as fp:
            json.dump(data_list, fp)

    data_info.projects_num = len(project_list)
    with open(static_dir + '/projects.list', 'w') as fp:
        fp.write('\n'.join(project_list))
    data_info.revisions_num = len(revision_set)
    with open(static_dir + '/revisions.list', 'w') as fp:
        fp.write('\n'.join(revision_set))


def paths_to_json_file(paths):
    path_list = []
    for path, item_list in paths.items():
        path_list.append(path)
        data_list = []
        for item in item_list:
            data = {
                'manifest': item.manifest,
                'project': item.project,
                'path': path,
                'revision': item.revision
            }
            data_list.append(data)

        file_name = result_paths_dir + '/' + quote(path, safe='')
        file_name = file_name.strip()
        with open(file_name, 'w') as fp:
            json.dump(data_list, fp)

    with open(static_dir + '/paths.list', 'w') as fp:
        fp.write('\n'.join(path_list))


def write_manifest_list_to_file():
    files = os.listdir(result_manifests_dir)
    manifest_file_list = list(map(lambda it: unquote(it), files))
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
