# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)

resouce_property_models = {
    "provider": [
        "secret_id",
        "secret_key",
        "region"
    ],
    "vpc": [
        "name",
        "cidr"
    ],
    "subnet": [
        "cidr",
        "name",
        "vpc_id",
        "zone"
    ],
    "route_table": [
        "name",
        "vpc_id"
    ],
    "route_entry": [
        "name",
        "vpc_id",
        "route_table_id",
        "next_type",
        "next_hub",
        "destination"
    ],
    "security_group": [
        "name",
        "vpc_id"
    ],
    "security_group_rule": [
        "description",
        "type",
        "security_group_id",
        "cidr_ip",
        "policy",
        "ip_protocol",
        "ports"
    ],
    "nat": [
        "name",
        "vpc_id",
        "subnet_id",
        "eip"
    ],
    "eip": [
        "name"
    ],
    "eip_association": [
        "name",
        "eip_id"
    ],
    "lb": [
    ],
    "disk": [
        "name",
        "type",
        "size",
        "zone"
    ],
    "disk_attach": [
        "disk_id",
        "instance_id"
    ],
    "instance": [
        "name",
        "hostname",
        "instance_type",
        "disk_type",
        "disk_size",
        "subnet_id",
        "zone",
        "image",
        "power_action",
        "force_delete"
    ],
    "mysql": [
        "name",
        "engine",
        "zone",
        "version",
        "disk_type",
        "disk_size",
        "subnet_id",
        "instance_type",
        "port",
        "user",
        "password",
        "force_delete"
    ],
    "mariadb": [
        "name",
        "engine",
        "zone",
        "version",
        "disk_type",
        "disk_size",
        "subnet_id",
        "instance_type",
        "port",
        "user",
        "password",
        "force_delete"
    ],
    "postgreSQL": [
        "name",
        "engine",
        "zone",
        "version",
        "disk_type",
        "disk_size",
        "subnet_id",
        "instance_type",
        "port",
        "user",
        "password",
        "force_delete"
    ],
    "rds": [
        "name",
        "engine",
        "zone",
        "version",
        "disk_type",
        "disk_size",
        "subnet_id",
        "instance_type",
        "port",
        "user",
        "password",
        "force_delete"
    ],
    "nosql": [
        "name",
        "engine",
        "zone",
        "version",
        "subnet_id",
        "instance_type",
        "port",
        "password",
        "force_delete"
    ],
    "mongodb": [
        "name",
        "engine",
        "zone",
        "version",
        "subnet_id",
        "instance_type",
        "port",
        "password",
        "force_delete"
    ],
    "kvstore": [
        "name",
        "engine",
        "zone",
        "version",
        "subnet_id",
        "instance_type",
        "port",
        "password",
        "force_delete"
    ],
    "redis": [
        "name",
        "engine",
        "zone",
        "version",
        "subnet_id",
        "instance_type",
        "port",
        "password",
        "force_delete"
    ],
    "memcached": [
        "name",
        "engine",
        "zone",
        "version",
        "subnet_id",
        "instance_type",
        "port",
        "password",
        "force_delete"
    ],
}

output_property_models = {
    "instance": [
        "ipaddress"
    ],
}


def property_necessary(resource_name, resource_property):
    if resource_name not in resouce_property_models.keys():
        return

    columns_property = resouce_property_models.get(resource_name)
    for column in columns_property:
        if column not in resource_property.keys():
            raise ValueError("缺少必要的property: %s" % column)


def output_necessary(resource_name, output_property):
    if resource_name not in output_property_models.keys():
        return

    columns_property = output_property_models.get(resource_name)
    for column in columns_property:
        if column not in output_property.keys():
            raise ValueError("缺少必要的output property: %s" % column)