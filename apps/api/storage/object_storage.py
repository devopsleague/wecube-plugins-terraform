# coding: utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

import json
import traceback
from lib.logs import logger
from lib.json_helper import format_json_dumps
from core import local_exceptions
from apps.api.configer.provider import ProviderApi
from apps.api.apibase import ApiBase
from apps.background.resource.storage.object_storage import ObjectStorageObject


class ObjectStorageApi(ApiBase):
    def __init__(self):
        super(ObjectStorageApi, self).__init__()
        self.resource_name = "object_storage"
        self.resource_workspace = "object_storage"
        self.resource_object = ObjectStorageObject()
        self.resource_keys_config = None

    def before_keys_checks(self, provider):
        '''

        :param provider:
        :param vpc_id:
        :return:
        '''

        self.resource_info(provider)
        return {}

    def save_data(self, rid, name, acl, url,
                  provider, provider_id, region, zone,
                  extend_info, define_json,
                  status, result_json):
        '''

        :param rid:
        :param name:
        :param type:
        :param size:
        :param provider:
        :param provider_id:
        :param region:
        :param zone:
        :param extend_info:
        :param define_json:
        :param status:
        :param result_json:
        :return:
        '''

        self.resource_object.create(create_data={"id": rid, "provider": provider,
                                                 "region": region, "zone": zone,
                                                 "name": name, "acl": acl,
                                                 "url": url, "status": status,
                                                 "provider_id": provider_id,
                                                 "extend_info": json.dumps(extend_info),
                                                 "define_json": json.dumps(define_json),
                                                 "result_json": json.dumps(result_json)})

    def create(self, rid, name, provider_id, acl, appid,
               zone, region, extend_info):

        '''

        :param rid:
        :param name:
        :param provider_id:
        :param type:
        :param size:
        :param zone:
        :param region:
        :param extend_info:
        :return:
        '''

        if appid:
            name = "%s-%s" % (name, appid)

        extend_info = extend_info or {}
        create_data = {"name": name, "acl": acl}
        label_name = self.resource_name + "_" + rid

        provider_object, provider_info = ProviderApi().provider_info(provider_id, region)
        _relations_id_dict = self.before_keys_checks(provider_object["name"])

        create_data.update(_relations_id_dict)
        define_json = self._generate_resource(provider_object["name"],
                                              label_name=label_name,
                                              data=create_data, extend_info=extend_info)

        output_json = self._generate_output(label_name=label_name)
        define_json.update(provider_info)
        define_json.update(output_json)

        _path = self.create_workpath(rid,
                                     provider=provider_object["name"],
                                     region=region)

        self.save_data(rid, name=name,
                       provider=provider_object["name"],
                       provider_id=provider_id,
                       region=region, zone=zone,
                       acl=acl, url="",
                       extend_info=extend_info,
                       define_json=define_json,
                       status="applying", result_json={})

        self.write_define(rid, _path, define_json=define_json)
        result = self.run(_path)

        result = self.formate_result(result)
        logger.info(format_json_dumps(result))

        _update_data = {"status": "ok", "result_json": format_json_dumps(result)}
        _update_data.update(self._read_output_result(result))

        if not _update_data.get("resource_id"):
            _update_data["resource_id"] = self._fetch_id(result)

        self.update_data(rid, data=_update_data)

        return rid

    def destory(self, rid):
        '''

        :param rid:
        :return:
        '''

        resource_info = self.resource_object.show(rid)
        _path = self.create_workpath(rid,
                                     provider=resource_info["provider"],
                                     region=resource_info["region"])

        if not self.destory_ensure_file(rid, path=_path):
            self.write_define(rid, _path, define_json=resource_info["define_json"])

        status = self.run_destory(_path)
        if not status:
            raise local_exceptions.ResourceOperateException(self.resource_name,
                                                            msg="delete %s %s failed" % (self.resource_name, rid))

        return self.resource_object.delete(rid)
