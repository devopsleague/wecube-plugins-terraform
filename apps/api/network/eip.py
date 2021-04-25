# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)

import json
import traceback
from lib.logs import logger
from lib.json_helper import format_json_dumps
from apps.common.convert_keys import define_relations_key
from apps.api.apibase import ApiBase
from apps.api.configer.provider import ProviderApi
from apps.background.resource.resource_base import CrsObject
from apps.api.apibase_backend import ApiBackendBase


class Common(object):
    def before_keys_checks(self, provider, create_data, is_update=None):
        '''

        :param provider:
        :return:
        '''

        self.resource_info(provider)
        return {}

    def generate_create_data(self, zone, create_data, **kwargs):
        r_create_data = {}
        create_data = {
            "name": create_data.get("name"),
            "charge_type": create_data.get("charge_type")
        }

        return create_data, r_create_data

    def generate_owner_data(self, create_data, **kwargs):
        owner_id = None
        return owner_id, None


class EipApi(Common, ApiBase):
    def __init__(self):
        super(EipApi, self).__init__()
        self.resource_name = "eip"
        self.resource_workspace = "eip"
        self._flush_resobj()
        self.resource_keys_config = None


class EipBackendApi(Common, ApiBase):
    def __init__(self):
        super(EipBackendApi, self).__init__()
        self.resource_name = "eip"
        self.resource_workspace = "eip"
        self._flush_resobj()
        self.resource_keys_config = None
