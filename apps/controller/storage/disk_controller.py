# _ coding:utf-8 _*_

from __future__ import (absolute_import, division, print_function, unicode_literals)

from core import validation
from core.controller import BackendController
from core.controller import BackendIdController
from core.controller import BaseController
from lib.uuid_util import get_uuid
from apps.api.storage.disk import DiskApi
from apps.api.storage.disk import DiskBackendApi
from apps.controller.source_controller import BaseSourceController


class ResBase(object):
    @classmethod
    def allow_key(cls, data):
        validation.allowed_key(data, ["id", "provider", "secret", "region", "zone",
                                      "name", "type", "size", "extend_info"])

    @classmethod
    def not_null(cls, data):
        validation.not_allowed_null(data=data,
                                    keys=["region", "provider", "name", "type", "size"]
                                    )

    @classmethod
    def validate_keys(cls, data):
        validation.validate_collector(data=data,
                                      strings=["id", "name", "region", "zone",
                                               "provider", "type", "secret"],
                                      ints=["size"],
                                      dicts=["extend_info"])

    @classmethod
    def create(cls, resource, data, **kwargs):
        rid = data.pop("id", None) or get_uuid()
        secret = data.pop("secret", None)
        region = data.pop("region", None)
        zone = data.pop("zone", None)
        provider = data.pop("provider", None)
        name = data.pop("name", None)
        disktype = data.pop("type", None)
        size = int(data.pop("size", None))

        asset_id = data.pop("asset_id", None)
        resource_id = data.pop("resource_id", None)

        extend_info = validation.validate_dict("extend_info", data.pop("extend_info", None))
        data.update(extend_info)

        create_data = {"name": name, "type": disktype, "size": size}
        _, result = resource.create(rid=rid, provider=provider,
                                    region=region, zone=zone,
                                    secret=secret,
                                    asset_id=asset_id,
                                    resource_id=resource_id,
                                    create_data=create_data,
                                    extend_info=data)

        res = {"id": rid, "resource_id": str(result.get("resource_id"))[:64]}
        return res, result


class DiskController(BackendController):
    allow_methods = ('GET', 'POST')
    resource = DiskApi()

    def list(self, request, data, orderby=None, page=None, pagesize=None, **kwargs):
        '''

        :param request:
        :param data:
        :param orderby:
        :param page:
        :param pagesize:
        :param kwargs:
        :return:
        '''

        validation.allowed_key(data, ["id", "provider", "region", 'resource_id',
                                      "provider_id", "name", "zone", "type", "enabled"])
        return self.resource.resource_object.list(filters=data, page=page,
                                                  pagesize=pagesize, orderby=orderby)

    def before_handler(self, request, data, **kwargs):
        ResBase.allow_key(data)
        ResBase.not_null(data)
        ResBase.validate_keys(data)

    def create(self, request, data, **kwargs):
        res, _ = ResBase.create(resource=self.resource, data=data)
        return 1, res


class DiskIdController(BackendIdController):
    allow_methods = ('GET', 'DELETE')
    resource = DiskApi()

    def show(self, request, data, **kwargs):
        '''

        :param request:
        :param data:
        :param kwargs:
        :return:
        '''

        rid = kwargs.pop("rid", None)
        return self.resource.resource_object.show(rid)

    def delete(self, request, data, **kwargs):
        rid = kwargs.pop("rid", None)
        return self.resource.destroy(rid)


class DiskAddController(BaseController):
    allow_methods = ("POST",)
    resource = DiskBackendApi()

    def before_handler(self, request, data, **kwargs):
        ResBase.not_null(data)
        ResBase.validate_keys(data)

    def response_templete(self, data):
        return {}

    def main_response(self, request, data, **kwargs):
        res, _ = ResBase.create(resource=self.resource, data=data)
        return res


class DiskDeleteController(BaseController):
    name = "Disk"
    resource_describe = "Disk"
    allow_methods = ("POST",)
    resource = DiskBackendApi()

    def before_handler(self, request, data, **kwargs):
        validation.not_allowed_null(data=data,
                                    keys=["id"]
                                    )

        validation.validate_string("id", data.get("id"))

    def response_templete(self, data):
        return {}

    def main_response(self, request, data, **kwargs):
        rid = data.pop("id", None)
        result = self.resource.destroy(rid)
        return {"result": result}


class DiskSourceController(BaseSourceController):
    name = "Disk"
    resource_describe = "Disk"
    allow_methods = ("POST",)
    resource = DiskBackendApi()

