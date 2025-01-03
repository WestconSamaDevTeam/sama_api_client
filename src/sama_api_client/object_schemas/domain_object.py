# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - Domain object schema
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# Date:      2024-12-31
#
# MIT License
#
# Copyright (c) 2024-present Westcon-Comstor
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Import required modules

from pydantic import BaseModel
from sama_api_client.object_schemas.link_object import LinkObject
from typing import Optional

# Example of the domain object as it is returned by the Check Mk REST API for a folder configuration:
#
# {
#     "links": [
#         {
#             "domainType": "link",
#             "rel": "self",
#             "href": "",
#             "method": "GET",
#             "type": "application/json",
#         }
#     ],
#     "id": "folder_config",
#     "domainType": "folder_config",
#     "value": [
#         {
#             "links": [
#                 {
#                     "domainType": "link",
#                     "rel": "self",
#                     "href": "",
#                     "method": "GET",
#                     "type": "application/json",
#                 },
#                 {
#                     "domainType": "link",
#                     "rel": "urn:org.restfulobjects:rels/update",
#                     "href": "",
#                     "method": "PUT",
#                     "type": "application/json",
#                 },
#                 {
#                     "domainType": "link",
#                     "rel": "urn:org.restfulobjects:rels/delete",
#                     "href": "",
#                     "method": "DELETE",
#                     "type": "application/json",
#                 },
#             ],
#             "domainType": "folder_config",
#             "id": "",
#             "title": "",
#             "members": {},
#             "extensions": {
#                 "path": "/",
#                 "attributes": {
#                     "site": "",
#                     "contactgroups": {
#                         "groups": [""],
#                         "use": True,
#                         "use_for_services": False,
#                         "recurse_use": False,
#                         "recurse_perms": False,
#                     },
#                     "parents": [""],
#                     "meta_data": {
#                         "created_at": "",
#                         "updated_at": "",
#                         "created_by": "",
#                     },
#                     "tag_CustomerID": "",
#                     "tag_SIGMA-CON": "",
#                     "tag_agent": "",
#                 },
#             },
#         }
#     ],
#     "extensions": {},
# }
#
# The domain object is a complex object that can contain multiple links and values.
# If the value is defined, it is a list of domain objects.
# The domain object can contain multiple links, values and extensions, which can be nested.
#
# The domain object was observed to return with at least the following keys, not all keys are always present:
#
# - links: list of link objects
# - id: string
# - instanceId: string
# - domainType: string
# - title: string
# - members: dictionary
# - value: list of domain objects
# - values: list of domain objects
# - extensions: dictionary
# - resultType: string
# - result: list of domain objects
#
# Also, it is known that in some cases the response object will contain a header called ETag, which is a string.
# This header is added to the domain object as an attribute.
# We need to keep this in mind that the domain object has this, and process it accordingly in the code.
#


class DomainObject(BaseModel):
    links: list[LinkObject]
    id: str
    instanceId: Optional[str] = None
    domainType: str
    title: Optional[str] = None
    members: Optional[dict] = None
    value: Optional[list["DomainObject"]] = None
    values: Optional[list["DomainObject"]] = None
    extensions: Optional[dict] = None
    resultType: Optional[str] = None
    result: Optional[list["DomainObject"]] = None
    ETag: Optional[str] = None
