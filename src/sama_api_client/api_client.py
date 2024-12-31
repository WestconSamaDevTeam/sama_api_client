# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - API client.
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

from typing import Optional
from sama_api_client.api_core import SamaApiClientCore
from requests.models import Response

from sama_api_client.object_schemas.domain_object import DomainObject
from sama_api_client.object_schemas.version_object import VersionObject


class SamaApiClient(SamaApiClientCore):
    def __init__(self, site_id: str, server_url: str, path: str) -> None:
        super().__init__(site_id=site_id, server_url=server_url)
        self.load_endpoints(path)

    def get_version_information(self) -> Optional[VersionObject]:
        resp: Optional[Response] = self.api_request("Version")
        if resp is None:
            return None
        result: VersionObject = VersionObject(**resp.json())
        return result

    def request(
        self,
        endpoint_name: str,
        no_default_headers: bool = False,
        data: Optional[str] = None,
        url_data: Optional[str] = None,
        params: Optional[dict] = None,
    ) -> Optional[DomainObject]:
        resp: Optional[Response] = self.api_request(
            endpoint_name, no_default_headers, data, url_data, params
        )
        if resp is None:
            return None
        result: DomainObject = DomainObject(**resp.json())
        return result
