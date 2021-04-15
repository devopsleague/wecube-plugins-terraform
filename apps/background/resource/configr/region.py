# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)

import json
import datetime
from core import local_exceptions
from lib.uuid_util import get_uuid
from apps.background.models.dbserver import RegionManager
from apps.background.models.dbserver import ZoneManager


class _AreaObject(object):
    def __init__(self):
        self.resource = None

    def list(self, filters=None, page=None, pagesize=None, orderby=None):
        filters = filters or {}
        filters["is_deleted"] = 0

        count, results = self.resource.list(filters=filters, pageAt=page,
                                            pageSize=pagesize, orderby=orderby)
        data = []
        for res in results:
            res["extend_info"] = json.loads(res["extend_info"])
            data.append(res)

        return count, data

    def create(self, create_data):
        create_data["id"] = create_data.get("id") or get_uuid()
        create_data["created_time"] = datetime.datetime.now()
        create_data["updated_time"] = create_data["created_time"]
        return self.resource.create(data=create_data)

    def show(self, rid, where_data=None):
        where_data = where_data or {}
        where_data.update({"id": rid, "is_deleted": 0})

        data = self.resource.get(filters=where_data)
        if data:
            data["extend_info"] = json.loads(data["extend_info"])

        return data

    def query_one(self, where_data):
        where_data = where_data or {}
        where_data.update({"is_deleted": 0})
        data = self.resource.get(filters=where_data)
        if data:
            data["extend_info"] = json.loads(data["extend_info"])

        return data

    def update(self, rid, update_data, where_data=None):
        where_data = where_data or {}
        where_data.update({"id": rid, "is_deleted": 0})
        update_data["updated_time"] = datetime.datetime.now()
        count, data = self.resource.update(filters=where_data, data=update_data)
        if data:
            data["extend_info"] = json.loads(data["extend_info"])

        return count, data

    def delete(self, rid, where_data=None):
        where_data = where_data or {}
        where_data.update({"id": rid})
        return self.resource.delete(filters=where_data)

    def ora_delete(self, rid):
        return self.resource.delete(filters={"id": rid})


class RegionObject(_AreaObject):
    def __init__(self):
        super(RegionObject, self).__init__()
        self.resource = RegionManager()

    def region_object(self, region_id):
        data = self.show(rid=region_id)
        if not data:
            raise local_exceptions.ResourceValidateError("region", "region %s 未注册" % region_id)
        return data

    def region_name_object(self, region, provider):
        data = self.query_one(where_data={"name": region, "provider": provider})
        if not data:
            raise local_exceptions.ResourceValidateError("region", "region %s 未注册" % region)
        return data


class ZoneObject(_AreaObject):
    def __init__(self):
        super(ZoneObject, self).__init__()
        self.resource = ZoneManager()

    def zone_object(self, zone_id):
        data = self.show(rid=zone_id)
        if not data:
            raise local_exceptions.ResourceValidateError("zone", "zone %s 未注册" % zone_id)
        return data

    def zone_name_object(self, zone, provider):
        data = self.query_one(where_data={"name": zone, "provider": provider})
        if not data:
            raise local_exceptions.ResourceValidateError("zone", "zone %s 未注册" % zone)
        return data
