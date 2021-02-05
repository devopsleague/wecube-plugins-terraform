# coding: utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

import base64
import json
from core import local_exceptions
from lib.logs import logger
from lib.json_helper import format_json_dumps
from apps.api.configer.provider import ProviderApi
from apps.common.convert_keys import define_relations_key
from apps.api.apibase import ApiBase
from apps.background.resource.resource_base import CrsObject


class MysqlDatabaseApi(ApiBase):
    def __init__(self):
        super(MysqlDatabaseApi, self).__init__()
        self.resource_name = "mysql_database"
        self.resource_workspace = "mysql_database"
        self.owner_resource = "mysql"
        self._flush_resobj()
        self.resource_keys_config = None

    def before_keys_checks(self, provider, create_data):
        '''

        :param provider:
        :param mysql_id:
        :return:
        '''

        mysql_id = create_data.get("mysql_id")

        self.resource_info(provider)
        resource_property = self.resource_keys_config["resource_property"]
        _mysql_status = define_relations_key("mysql_id", mysql_id, resource_property.get("mysql_id"))

        ext_info = {}
        if mysql_id and (not _mysql_status):
            ext_info["mysql_id"] = CrsObject("mysql").object_resource_id(mysql_id)

        logger.info("before_keys_checks add info: %s" % (format_json_dumps(ext_info)))
        return ext_info

    # def check_database(self, mysql_id, database):
    #     _exists_data = MysqlDatabaseObject().query_one(where_data={"name": database, "rds_id": mysql_id})
    #     if _exists_data:
    #         raise local_exceptions.ResourceValidateError("database name", "database %s already exists" % database)

    def create(self, rid, name, provider_id, mysql_id,
               zone, region, extend_info, **kwargs):

        '''

        :param rid:
        :param name:
        :param provider_id:
        :param mysql_id:
        :param zone:
        :param region:
        :param extend_info:
        :param kwargs:
        :return:
        '''

        _exists_data = self.create_resource_exists(rid)
        if _exists_data:
            return _exists_data

        extend_info = extend_info or {}

        create_data = {"name": name}
        _r_create_data = {"mysql_id": mysql_id}

        # self.check_database(mysql_id, name)
        provider_object, provider_info = ProviderApi().provider_info(provider_id, region)
        _relations_id_dict = self.before_keys_checks(provider_object["name"], _r_create_data)

        create_data.update(_relations_id_dict)

        count, res = self.run_create(rid, provider_id, region, zone=zone,
                                     provider_object=provider_object,
                                     provider_info=provider_info,
                                     owner_id=mysql_id,
                                     relation_id=None,
                                     create_data=create_data,
                                     extend_info=extend_info, **kwargs)

        return count, res
