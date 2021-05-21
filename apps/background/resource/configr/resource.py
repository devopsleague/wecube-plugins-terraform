# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)

import json
import datetime
import traceback
from lib.logs import logger
from lib.uuid_util import get_uuid
from apps.background.models.dbserver import ResourceManager


class ResourceObject(object):
    def __init__(self):
        self.resource = ResourceManager()

    def list(self, filters=None, page=None,
             pagesize=None, orderby=None,
             filter_string=None, filter_in=None):
        '''

        :param filters:
        :param page:
        :param pagesize:
        :param orderby:
        :param filter_string:
        :param filter_in:
        :return:
        '''

        filter_in = filter_in or {}
        for key, value in filter_in.items():
            if value:
                f = ''
                for x in value:
                    f += "'" + x + "',"
                f = f[:-1]

                x = '(' + f + ')'
                if filter_string:
                    filter_string += 'and ' + key + " in " + x + " "
                else:
                    filter_string = key + " in " + x + " "

        count, results = self.resource.list(filters=filters, pageAt=page,
                                            filter_string=filter_string,
                                            pageSize=pagesize, orderby=orderby)
        data = []
        for res in results:
            res["extend_info"] = json.loads(res["extend_info"])
            res["resource_property"] = json.loads(res["resource_property"])
            res["resource_output"] = json.loads(res["resource_output"]) if res["resource_output"] else {}
            res["data_source"] = json.loads(res["data_source"]) if res.get("data_source") else {}
            t = json.loads(res["data_source_output"]) if res.get("data_source_output") else {}
            res["data_source_output"] = t
            res["pre_action_output"] = json.loads(res["pre_action_output"]) if res.get("pre_action_output") else {}
            data.append(res)

        return count, data

    def create(self, create_data):
        create_data["id"] = create_data.get("id") or get_uuid()
        create_data["created_time"] = datetime.datetime.now()
        create_data["updated_time"] = create_data["created_time"]
        return self.resource.create(data=create_data)

    def show(self, rid, where_data=None):
        where_data = where_data or {}
        where_data.update({"id": rid})
        return self.query_one(where_data)

    def query_one(self, where_data):
        data = self.resource.get(filters=where_data)
        if data:
            data["extend_info"] = json.loads(data["extend_info"])
            data["resource_property"] = json.loads(data["resource_property"])
            data["resource_output"] = json.loads(data["resource_output"]) if data["resource_output"] else {}
            data["data_source"] = json.loads(data["data_source"]) if data.get("data_source") else {}
            t = json.loads(data["data_source_output"]) if data.get("data_source_output") else {}
            data["data_source_output"] = t
            data["pre_action_output"] = json.loads(data["pre_action_output"]) if data.get("pre_action_output") else {}
        return data

    def update(self, rid, update_data, where_data=None):
        where_data = where_data or {}
        where_data.update({"id": rid})
        update_data["updated_time"] = datetime.datetime.now()
        count, data = self.resource.update(filters=where_data, data=update_data)
        if data:
            data["extend_info"] = json.loads(data["extend_info"])
            data["resource_property"] = json.loads(data["resource_property"])
            data["resource_output"] = json.loads(data["resource_output"]) if data["resource_output"] else {}
            data["data_source"] = json.loads(data["data_source"]) if data.get("data_source") else {}
            t = json.loads(data["data_source_output"]) if data.get("data_source_output") else {}
            data["data_source_output"] = t
            data["pre_action_output"] = json.loads(data["pre_action_output"]) if data.get("pre_action_output") else {}
        return count, data

    def delete(self, rid, where_data=None):
        where_data = where_data or {}
        where_data.update({"id": rid})
        return self.resource.delete(filters=where_data)

    def ora_delete(self, rid):
        return self.resource.delete(filters={"id": rid})
