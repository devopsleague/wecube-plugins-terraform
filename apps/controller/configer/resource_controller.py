# _ coding:utf-8 _*_

from __future__ import (absolute_import, division, print_function, unicode_literals)

import json
import copy
from lib.uuid_util import get_uuid
from core import validation
from core.controller import BackendController
from core.controller import BackendIdController
from apps.common.convert_keys import validate_convert_key
from apps.common.convert_keys import validate_convert_value
from apps.api.configer.resource import ResourceObject
from apps.api.configer.provider import ProviderObject
from .model_args import output_property_models
from .model_args import property_necessary
from .model_args import output_necessary
from .model_args import source_necessary
from .model_args import data_source_output_necessary


def format_argument(key, data):
    if not data:
        return ""
    if isinstance(data, dict):
        return data
    elif isinstance(data, basestring):
        data = data.strip()
        if data.startswith("{"):
            try:
                json.loads(data)
            except:
                try:
                    eval(data)
                except:
                    raise ValueError("data: %s is not json " % (data))

        return data
    else:
        raise ValueError("key: %s 应为json或string" % key)


def get_columns(defines):
    result = []
    for key, define in defines.items():
        if isinstance(define, basestring):
            result.append(key)
        elif isinstance(define, dict):
            if define.get("define"):
                result.append(key)
                result += get_columns(defines.get("define"))
            else:
                tkey = define.get("convert") or key
                result.append(tkey)
        else:
            pass

    return result


class ResourceController(BackendController):
    resource = ResourceObject()

    def list(self, request, data, orderby=None, page=None, pagesize=None, **kwargs):
        validation.allowed_key(data, ["id", "provider", "resource_type", "resource_name",
                                      "data_source_argument", "data_source_name"])

        filter_string = None
        for key in ["resource_type", "provider", "resource_name", "data_source_name"]:
            if data.get(key):
                if filter_string:
                    filter_string += 'and ' + key + " like '%" + data.get(key) + "%' "
                else:
                    filter_string = key + " like '%" + data.get(key) + "%' "
                data.pop(key, None)

        return self.resource.list(filters=data, page=page,
                                  filter_string=filter_string,
                                  pagesize=pagesize, orderby=orderby)

    def before_handler(self, request, data, **kwargs):
        validation.allowed_key(data, ["id", "provider", "resource_type", "extend_info",
                                      "resource_name", "resource_property", "resource_output",
                                      "data_source", "data_source_name",
                                      "pre_action", "pre_action_output",
                                      "data_source_output", "data_source_argument"])
        validation.not_allowed_null(data=data,
                                    keys=["provider", "resource_type"]
                                    )

        validation.validate_string("id", data.get("id"))
        validation.validate_string("provider", data["provider"])
        validation.validate_string("resource_type", data.get("resource_type"))

        # for resource
        validation.validate_string("resource_name", data.get("resource_name"))
        validation.validate_dict("extend_info", data.get("extend_info"))
        validation.validate_dict("resource_property", data.get("resource_property"))
        validation.validate_dict("resource_output", data.get("resource_output"))

        # for data source
        validation.validate_string("data_source_name", data.get("data_source_name"))
        validation.validate_string("data_source_argument", data.get("data_source_argument"))
        validation.validate_dict("data_source", data.get("data_source"))
        validation.validate_dict("data_source_output", data.get("data_source_output"))

        # pre action
        validation.validate_dict("pre_action_output", data.get("pre_action_output"))
        validation.validate_string("pre_action", data.get("pre_action"))

    def create(self, request, data, **kwargs):
        '''

        :param request:
        :param data:
        extend_info： {}  define example: {"version": "v1.1.0"}
        resource_property ｛｝define property for provider， example secret_key to key
        define example: {"secret_key": "key"}
        :param kwargs:
        :return:
        '''

        # resource
        extend_info = validation.validate_dict("extend_info", data.get("extend_info")) or {}
        resource_property = validation.validate_dict("resource_property", data.get("resource_property")) or {}
        resource_output = validation.validate_dict("resource_output", data.get("resource_output")) or {}

        data_source = validation.validate_dict("data_source", data.get("data_source"))
        data_source_output = validation.validate_dict("data_source_output", data.get("data_source_output"))

        pre_action_output = validation.validate_dict("pre_action_output", data.get("pre_action_output"))
        for _, value in pre_action_output.items():
            if not isinstance(value, basestring):
                raise ValueError("pre_action_output 为key-value定义")
        if len(pre_action_output) > 1:
            raise ValueError("output 只支持最多一个参数过滤")

        resource_property = validate_convert_key(resource_property)
        validate_convert_value(extend_info)
        validate_convert_value(resource_output)
        data_source_output = validate_convert_key(data_source_output)
        property_necessary(resource_name=data["resource_type"],
                           resource_property=resource_property)

        output_necessary(resource_name=data["resource_type"],
                         resource_output=resource_output)

        source_necessary(resource_name=data["resource_type"],
                         data_source=data_source)

        data_source_output_necessary(resource_name=data["resource_type"],
                                     resource_property=data_source_output)

        data_source_argument = format_argument("data_source_argument", data.get("data_source_argument"))

        resource_name = data.get("resource_name", "") or ""
        ProviderObject().provider_name_object(data["provider"])
        create_data = {"id": data.get("id") or get_uuid(),
                       "provider": data["provider"],
                       "resource_type": data.get("resource_type"),
                       "resource_name": resource_name,
                       "extend_info": json.dumps(extend_info),
                       "resource_property": json.dumps(resource_property),
                       "resource_output": json.dumps(resource_output),
                       "data_source_name": data.get("data_source_name"),
                       "data_source_argument": data_source_argument,
                       "data_source_output": json.dumps(data_source_output),
                       "data_source": json.dumps(data_source),
                       "pre_action": data.get("pre_action"),
                       "pre_action_output": json.dumps(pre_action_output)
                       }

        return self.resource.create(create_data)


class ResourceIdController(BackendIdController):
    resource = ResourceObject()

    def show(self, request, data, **kwargs):
        rid = kwargs.pop("rid", None)
        return self.resource.show(rid)

    def before_handler(self, request, data, **kwargs):
        validation.allowed_key(data, ["provider", "resource_type", "extend_info",
                                      "resource_name", "resource_property",
                                      "enabled", "resource_output",
                                      "data_source", "data_source_name",
                                      "data_source_output", "pre_action",
                                      "pre_action_output",
                                      "data_source_argument"])

        validation.validate_string("provider", data["provider"])
        validation.validate_string("resource_type", data.get("resource_type"))

        # for resource
        validation.validate_string("resource_name", data.get("resource_name"))
        validation.validate_dict("extend_info", data.get("extend_info"))
        validation.validate_dict("resource_property", data.get("resource_property"))
        validation.validate_dict("resource_output", data.get("resource_output"))

        # for data source
        validation.validate_string("data_source_name", data.get("data_source_name"))
        validation.validate_string("data_source_argument", data.get("data_source_argument"))

        # pre action
        validation.validate_string("pre_action", data.get("pre_action"))
        validation.validate_dict("pre_action_output", data.get("pre_action_output"))

        format_argument("data_source_argument", data.get("data_source_argument"))
        validation.validate_dict("data_source", data.get("data_source"))
        validation.validate_dict("data_source_output", data.get("data_source_output"))

    def update(self, request, data, **kwargs):
        rid = kwargs.pop("rid", None)
        if data.get("extend_info") is not None:
            extend_info = validation.validate_dict("extend_info", data.get("extend_info"))
            validate_convert_value(extend_info)
            data["extend_info"] = json.dumps(extend_info)

        if data.get("resource_property") is not None:
            resource_property = validation.validate_dict("resource_property", data.get("resource_property")) or {}
            resource_property = validate_convert_key(resource_property)
            property_necessary(resource_name=data["resource_type"],
                               resource_property=resource_property)

            data["resource_property"] = json.dumps(resource_property)

        if data.get("resource_output") is not None:
            resource_output = validation.validate_dict("resource_output", data.get("resource_output")) or {}
            validate_convert_value(resource_output)
            output_necessary(resource_name=data["resource_type"],
                             resource_output=resource_output)

            data["resource_output"] = json.dumps(resource_output)

        if data.get("data_source") is not None:
            data_source = validation.validate_dict("data_source", data.get("data_source"))
            source_necessary(resource_name=data["resource_type"],
                             data_source=data_source)

            data["data_source"] = json.dumps(data_source)

        if data.get("data_source_output") is not None:
            data_source_output = validation.validate_dict("data_source_output", data.get("data_source_output"))
            data_source_output = validate_convert_key(data_source_output)

            data_source_output_necessary(resource_name=data["resource_type"],
                                         resource_property=data_source_output)

            for _, value in data_source_output.items():
                if not isinstance(value, (basestring, dict)):
                    raise ValueError("data_source_output 为key-value定义")

            data["data_source_output"] = json.dumps(data_source_output)

        if data.get("pre_action_output") is not None:
            pre_action_output = validation.validate_dict("pre_action_output", data.get("pre_action_output"))

            for _, value in pre_action_output.items():
                if not isinstance(value, basestring):
                    raise ValueError("data_source_output 为key-value定义")

            if len(pre_action_output) > 1:
                raise ValueError("output 只支持最多一个参数过滤")

            data["pre_action_output"] = json.dumps(pre_action_output)

        if "provider" in data.keys():
            if not data.get("provider"):
                raise ValueError("provider 不能为空")
            ProviderObject().provider_name_object(data["provider"])

        return self.resource.update(rid, data)

    def delete(self, request, data, **kwargs):
        rid = kwargs.pop("rid", None)
        return self.resource.delete(rid)


class ResourceListController(BackendIdController):
    resource = ResourceObject()
    allow_methods = ('GET',)

    def get_resource_list(self, data):
        filter_string = None
        _, resource_lists = self.resource.list(filters=data, page=1, filter_string=filter_string,
                                               pagesize=10000, orderby=None)

        res = []
        for xres in resource_lists:
            res.append(xres["resource_type"])

        return list(set(res))

    def show(self, request, data, **kwargs):
        provider = data.get("provider")
        if provider:
            config_columns = self.get_resource_list(data={"provider": provider})
            columns = output_property_models.keys() + config_columns
        else:
            columns = output_property_models.keys()

        columns = list(set(columns))
        res = []
        for column in columns:
            res.append({"id": column, "name": column})

        return {"resource": res}


class ResourceAttrController(BackendIdController):
    resource = ResourceObject()
    allow_methods = ('GET',)

    def show(self, request, data, **kwargs):
        validation.allowed_key(data, ["resource_type", "provider"])
        validation.not_allowed_null(["resource_type", "provider"], data)

        define_data = self.resource.query_one(where_data={"provider": data.get("provider"),
                                                          "resource_type": data.get("resource_type")})

        define = define_data.get("resource_property") or {}
        out_define = define_data.get("resource_output") or {}

        columns = get_columns(define) + get_columns(out_define)
        columns = list(set(columns))

        res = []
        for column in columns:
            res.append({"id": column, "name": column})

        return {"resource": res}


class HintResourceController(BackendIdController):
    resource = ResourceObject()
    allow_methods = ('GET',)

    def format_resource_type(self, datas):
        models = copy.deepcopy(output_property_models)
        for data in datas:
            resource_type = data.get("resource_type")
            if models.get(resource_type):
                r_out = data.get("resource_output") or {}
                tmp = models[resource_type]
                models[resource_type] = list(set(r_out.keys() + tmp))
            # else:
            #     tmp = data.get("resource_output") or {}
            #     models[resource_type] = tmp.keys()

        return models

    def get_resource_list(self, data):
        filter_string = None
        _, resource_lists = self.resource.list(filters=data, page=1, filter_string=filter_string,
                                               pagesize=10000, orderby=None)
        return resource_lists

    def show(self, request, data, **kwargs):
        validation.allowed_key(data, ["resource_type"])
        resource_attribute = self.format_resource_type(self.get_resource_list(data))

        result = ["$zone", "$region", "$instance.type",
                  "$instance.type.cpu", "$instance.type.memory", "$resource"]

        for xres in resource_attribute.keys():
            result.append("$resource.%s" % (xres))

        res = []
        for column in result:
            res.append({"id": column, "name": column})

        return {"resource": res, "attribute": resource_attribute}
