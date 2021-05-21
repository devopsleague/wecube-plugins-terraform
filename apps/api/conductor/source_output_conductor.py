# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)

import re
import json
import traceback
from lib.logs import logger
from apps.api.conductor.type_format import TypeFormat
from apps.api.conductor.model_format import ModelFormat
from apps.api.conductor.value_conductor import ValueConfigerConductor


class SourceOuterReader(object):
    @staticmethod
    def format_argument(key, data):
        if not data:
            return ""
        if isinstance(data, dict):
            return data
        elif isinstance(data, basestring):
            data = data.strip()
            if data.startswith("{"):
                data = TypeFormat.f_dict(data)

            return data
        else:
            raise ValueError("key: %s 应为json或string" % key)

    @staticmethod
    def is_null_dict(data):
        count = 0
        for _, x_value in data.items():
            if not x_value:
                count += 1
        if count == len(data):
            logger.info("out data columns is null, skip ...")
            return True

        return False

    @staticmethod
    def skip_empty_dict(datas):
        result = []
        for out_data in datas:
            if out_data:
                if isinstance(out_data, dict) and (not SourceOuterReader.is_null_dict(out_data)):
                    result.append(out_data)

                result.append(out_data)

        return result

    @staticmethod
    def eval_line(line, column):
        def line_pointer(data):
            try:
                data = data[len("$line"):]
                nums = re.findall('\d+', data)
                if nums:
                    num = nums[0]
                    split_point = data.replace(num)
                    return split_point, int(num)
                else:
                    return None, None
            except:
                raise ValueError("$line define error, use: split + [num], example: $line / $line#2")

        if column == "$line":
            return line
        elif column.startswith("$line"):
            s_split, point = line_pointer(column)
            if s_split:
                try:
                    return line.split(s_split)[point]
                except:
                    raise ValueError("$line: %s 不能获取数据， 请检查定义" % column)
            else:
                return line
        else:
            logger.info("unknown define %s ,skip ..." % line)
            return ""

    @staticmethod
    def fetch_property(provider, key, data, define_column, resource_value_config):
        '''

        提取 output 数据字段值
        :param provider:
        :param data:
        :param define_columns:
        string: {"desc": "$line"}
        dict: {"name": "name", "dns": {"type": "list", "convert": "dns_info"}}
        :param resource_value_config:
        :return:
        '''

        def _f_string_property_(data, key, column, resource_value_config):
            '''
            #处理data为string时字段提取
            {"desc": "$line", "port": "$line#2"}
            :param data:
            :param key:
            :param columns:
            :param resource_values_config:
            :return:
            '''

            x_value = ""
            if column.startswith("$"):
                x_value = SourceOuterReader.eval_line(line=data, column=column)
                if x_value:
                    x_value = resource_value_config.get(x_value) or x_value

            return {key: x_value}

        def _f_fetch_property(data, define):
            if "." in define:
                _keys = define.split(".")
                tmp = data
                for x_key in _keys:
                    try:
                        tmp = tmp[int(x_key)]
                    except:
                        tmp = tmp.get(x_key)

                x_data = tmp
            else:
                x_data = data.get(define) or ""

            return x_data

        def _f_dict_property_(provider, data, key, define, resource_value_config):
            '''
            for dict
            :param data:
            :param define_columns:
            {"name": "name", "dns": {"type": "list", "convert": "dns_info"}}
            :param resource_value_config:
            :return:
            '''

            if not define:
                logger.info("key: %s define is empty, skip it .." % key)
                return {}

            if isinstance(define, basestring):
                if define == '-' or not define.strip():
                    logger.info("key: %s define ignore, skip it .." % key)
                    return {}

                value = _f_fetch_property(data, define)
                value = ValueConfigerConductor.outer_value(value, resource_value_config)
                return {key: value}
            else:
                to_column = define.get("convert") or key
                value = _f_fetch_property(data, to_column)
                value = ModelFormat.format_type(value, type=define.get("type", "string"))
                value = ValueConfigerConductor.outer_value(value, resource_value_config)

                # for hint 转换为资产id等信息
                value, add_info = ModelFormat.hint_outer_infos(provider, value, define)
                add_info[key] = value
                return add_info

        if isinstance(data, basestring):
            return _f_string_property_(data=data, key=key,
                                       column=define_column,
                                       resource_value_config=resource_value_config)

        return _f_dict_property_(provider=provider, data=data,
                                 key=key, define=define_column,
                                 resource_value_config=resource_value_config)


def source_object_outer(datas, columns):
    if len(columns) == 0:
        c_data = []
        for data in datas:
            if isinstance(data, list):
                c_data += data
            else:
                c_data.append(data)

        return SourceOuterReader.skip_empty_dict(c_data)

    column = columns.pop(0)
    if isinstance(datas, list):
        x_data = []
        for data in datas:
            try:
                x_data.append(data.get(column)) if data.get(column) else None
            except:
                raise ValueError("can not fetch property： %s" % column)

        return source_object_outer(x_data, columns)
    elif isinstance(datas, dict):
        return source_object_outer(datas.get(column), columns)
    else:
        logger.info("data is not dict/list, no columns %s filter, skip.." % column)
        return datas

