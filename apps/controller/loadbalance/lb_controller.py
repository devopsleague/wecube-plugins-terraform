# _ coding:utf-8 _*_

from __future__ import (absolute_import, division, print_function, unicode_literals)

from core import validation
from core.controller import BackendController
from core.controller import BackendIdController
from core.controller import BaseController
from lib.uuid_util import get_uuid
from apps.api.loadbalance.lb import LBApi
from apps.api.loadbalance.lb import LBBackendApi
from apps.controller.backend_controller import BackendAddController
from apps.controller.backend_controller import BackendDeleteController
from apps.controller.backend_controller import BackendSourceController


class ResBase(object):
    @classmethod
    def allow_key(cls, data):
        validation.allowed_key(data, ["id", "provider", "secret", "region", "zone",
                                      "name", "extend_info", "subnet_id",
                                      "network_type", "vpc_id", "charge_type"])

    @classmethod
    def not_null(cls, data):
        validation.not_allowed_null(data=data,
                                    keys=["region", "provider", "name", "subnet_id"]
                                    )

    @classmethod
    def validate_keys(cls, data):
        validation.validate_collector(data=data,
                                      strings=["id", "name", "region", "zone",
                                               "provider", "secret", "subnet_id",
                                               "network_type", "vpc_id", "charge_type"],
                                      dicts=["extend_info"])

    @classmethod
    def create(cls, resource, data, **kwargs):
        rid = data.pop("id", None) or get_uuid()
        secret = data.pop("secret", None)
        region = data.pop("region", None)
        zone = data.pop("zone", None)
        provider = data.pop("provider", None)
        name = data.pop("name", None)
        subnet_id = data.pop("subnet_id", None)
        vpc_id = data.pop("vpc_id", None)
        network_type = data.pop("network_type", None)
        charge_type = data.pop("charge_type", None)

        asset_id = data.pop("asset_id", None)
        resource_id = data.pop("resource_id", None)

        extend_info = validation.validate_dict("extend_info", data.pop("extend_info", None))
        data.update(extend_info)

        create_data = {"name": name, "vpc_id": vpc_id, "charge_type": charge_type,
                       "subnet_id": subnet_id, "network_type": network_type}
        _, result = resource.create(rid=rid, provider=provider,
                                    region=region, zone=zone,
                                    secret=secret,
                                    asset_id=asset_id,
                                    resource_id=resource_id,
                                    create_data=create_data,
                                    extend_info=data)

        res = {"id": rid, "ipaddress": result.get("ipaddress"),
               "resource_id": str(result.get("resource_id"))[:64]}
        return res, result


class LBController(BackendController):
    allow_methods = ('GET', 'POST')
    resource = LBApi()

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

        validation.allowed_key(data, ["id", "provider", "region", 'resource_id', "ipaddress",
                                      "provider_id", "name", "subnet_id", "enabled"])
        return self.resource.resource_object.list(filters=data, page=page,
                                                  pagesize=pagesize, orderby=orderby)

    def before_handler(self, request, data, **kwargs):
        ResBase.allow_key(data)
        ResBase.not_null(data)
        ResBase.validate_keys(data)

    def create(self, request, data, **kwargs):
        res, _ = ResBase.create(resource=self.resource, data=data)
        return 1, res


class LBIdController(BackendIdController):
    allow_methods = ('GET', 'DELETE', 'PATCH')
    resource = LBApi()

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


class LBIdDettachController(BackendIdController):
    allow_methods = ('PATCH',)
    resource = LBApi()

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


class LBAddController(BackendAddController):
    allow_methods = ("POST",)
    resource = LBBackendApi()


class LBDeleteController(BackendDeleteController):
    name = "LB"
    resource_describe = "LB"
    allow_methods = ("POST",)
    resource = LBBackendApi()


class LBSourceController(BackendSourceController):
    name = "LB"
    resource_describe = "LB"
    allow_methods = ("POST",)
    resource = LBBackendApi()
