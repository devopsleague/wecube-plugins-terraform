# _ coding:utf-8 _*_

from __future__ import (absolute_import, division, print_function, unicode_literals)

import json

from apps.api.configer.resource import ResourceObject
from core import validation
from core.controller import BackendController
from core.controller import BackendIdController
from lib.uuid_util import get_uuid


class ResourceController(BackendController):
    resource = ResourceObject()

    def list(self, request, data, orderby=None, page=None, pagesize=None, **kwargs):
        validation.allowed_key(data, ["id", "provider", "property", "resource_name"])
        return self.resource.list(filters=data, page=page,
                                  pagesize=pagesize, orderby=orderby)

    def before_handler(self, request, data, **kwargs):
        validation.allowed_key(data, ["id", "provider", "property", "extend_info",
                                      "resource_name", "resource_property"])
        validation.not_allowed_null(data=data,
                                    keys=["provider", "property",
                                          "resource_name", "resource_property"]
                                    )

        validation.validate_string("id", data.get("id"))
        validation.validate_string("provider", data["provider"])
        validation.validate_string("property", data.get("property"))
        validation.validate_string("resource_name", data.get("resource_name"))
        validation.validate_dict("extend_info", data.get("extend_info"))
        validation.validate_dict("resource_property", data.get("resource_property"))

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
        # todo 定义必要的标准property
        # todo 校验property定义合法性


        extend_info = validation.validate_dict("extend_info", data.get("extend_info")) or {}
        resource_property = validation.validate_dict("resource_property", data.get("resource_property")) or {}

        create_data = {"id": get_uuid(), "provider": data["provider"],
                       "property": data.get("property"),
                       "resource_name": data.get("resource_name"),
                       "extend_info": json.dumps(extend_info),
                       "resource_property": json.dumps(resource_property)
                       }

        return self.resource.create(create_data)


class ResourceIdController(BackendIdController):
    resource = ResourceObject()

    def show(self, request, data, **kwargs):
        rid = kwargs.pop("rid", None)
        return self.resource.show(rid)

    def before_handler(self, request, data, **kwargs):
        validation.allowed_key(data, ["provider", "property", "extend_info",
                                      "resource_name", "resource_property"])
        validation.not_allowed_null(data=data,
                                    keys=["provider", "property",
                                          "resource_name", "resource_property"]
                                    )

        validation.validate_string("provider", data["provider"])
        validation.validate_string("property", data.get("property"))
        validation.validate_string("resource_name", data.get("resource_name"))
        validation.validate_dict("extend_info", data.get("extend_info"))
        validation.validate_dict("resource_property", data.get("resource_property"))

    def update(self, request, data, **kwargs):
        rid = kwargs.pop("rid", None)
        if data.get("extend_info") is not None:
            data["extend_info"] = json.dumps(data.get("extend_info", {}))

        if data.get("resource_property") is not None:
            data["resource_property"] = json.dumps(data.get("resource_property", {}))
        return self.resource.update(rid, data)

    def delete(self, request, data, **kwargs):
        rid = kwargs.pop("rid", None)
        return self.resource.delete(rid)
