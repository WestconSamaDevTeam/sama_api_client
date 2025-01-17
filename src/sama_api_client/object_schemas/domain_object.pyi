# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - Domain object schema - type stub
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# Date:      2025-01-16
#
# MIT License
#
# Copyright (c) 2025-present Westcon-Comstor
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

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from sama_api_client.object_schemas.link_object import LinkObject

class DomainObject(BaseModel):
    links: List[LinkObject]
    id: str
    instanceId: Optional[str]
    domainType: str
    title: Optional[str]
    members: Optional[Dict[str, Any]]
    value: Optional[List["DomainObject"]]
    values: Optional[List["DomainObject"]]
    extensions: Optional[Dict[str, Any]]
    resultType: Optional[str]
    result: Optional[List["DomainObject"]]
    ETag: Optional[str]

    @staticmethod
    def Status204() -> "DomainObject": ...
