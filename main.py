# -*- coding: utf-8 -*-

import json
import os

import tools
from config import Config

from manifest import Manifest
from project import Project

__author__ = 'liying'


def read_config(config_file_name):
    """读取配置"""
    with open(config_file_name) as fp:
        config_obj = json.load(fp)

    local_config = Config()
    local_config.manifest_root_dir = config_obj.get('manifest_root_dir', 'manifests')
    local_config.manifest_dirs_for_query = config_obj.get('manifest_dirs_for_query', [])
    local_config.excluded_files = config_obj.get('excluded_files', [])
    manifest_file_list = config_obj.get('manifest_file_list', '')
    if manifest_file_list != '':
        with open(manifest_file_list) as fp:
            lines = fp.read().split('\n')
            for line in lines:
                if line.strip() != '':
                    local_config.manifest_file_list.append(line)

    local_config.ignore_parse_error = config_obj.get('ignore_parse_error', False)
    local_config.analysis_upstream_first = config_obj.get('analysis_upstream_first', True)
    local_config.frontend_static_dir = config_obj.get('frontend_static_dir', 'frontend/static')
    return local_config


def parse_manifest(root_dir, manifest_file_list, analysis_upstream_first, ignore_parse_error=False):
    """解析 manifest 文件"""
    project = Project()
    current_path = os.path.abspath('.')
    os.chdir(root_dir)
    for manifest_file in manifest_file_list:
        manifest = Manifest(manifest_file, analysis_upstream_first=analysis_upstream_first)
        try:
            item_dict, _, _, _ = manifest.parse()
        except Exception as e:
            if ignore_parse_error:
                # 忽略解析错误
                print('[ERROR]: Parsing error:', manifest_file)
                print(e)
                continue
            else:
                raise e

        project.add_manifest_and_dict(manifest_file, item_dict)
        os.chdir(current_path)
        tools.dict_to_json_file(manifest_file, item_dict)
        os.chdir(root_dir)

    os.chdir(current_path)
    tools.projects_to_json_file(project.projects)
    tools.paths_to_json_file(project.paths)


def get_manifest_file_list(config):
    """获取所有待解析的 manifest 文件列表"""
    current_path = os.path.abspath('.')
    os.chdir(config.manifest_root_dir)
    temp_manifest_file_list = config.manifest_file_list
    manifest_dirs_for_query = config.manifest_dirs_for_query
    for manifest_dir in manifest_dirs_for_query:
        for froot, dirs, files in os.walk(manifest_dir):
            for f in files:
                if f.endswith('.xml'):
                    manifest_file = os.path.join(froot, f).replace('\\', '/')
                    if manifest_file not in temp_manifest_file_list:
                        temp_manifest_file_list.append(manifest_file)

    manifest_file_list = []
    # 过滤
    for manifest in temp_manifest_file_list:
        if manifest not in config.excluded_files:
            manifest_file_list.append(manifest)
    os.chdir(current_path)
    return manifest_file_list
