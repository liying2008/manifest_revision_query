# -*- coding: utf-8 -*-

from main import *

__author__ = 'liying'

if __name__ == '__main__':
    config_file_name = 'config.json'
    # 读取配置
    config = read_config(config_file_name)
    # 检查前端 static 目录
    tools.check_static_dir(config.frontend_static_dir)
    # 获取需要解析的 manifest 文件列表
    manifest_file_list = get_manifest_file_list(config)
    # 解析 manifest 文件
    parse_manifest(config.manifest_root_dir, manifest_file_list, config.analysis_upstream_first,
                   config.ignore_parse_error)
    # 把解析完成的 manifest 文件列表写入 static 目录
    tools.write_manifest_list_to_file()
    # 把数据信息写入 static 目录
    tools.write_data_info_to_file()
