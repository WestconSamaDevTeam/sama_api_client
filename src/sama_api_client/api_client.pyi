# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - SAMA API client - type stub
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

from typing import Optional, Dict, Literal, final
from sama_api_client.api_core import RestApiClientCore
from sama_api_client.object_schemas.domain_object import DomainObject
from sama_api_client.object_schemas.version_object import VersionObject
from sama_api_client.configuration import API_DEFINITION_PATH

@final
class SamaApiClient(RestApiClientCore):
    def __init__(
        self, site_id: str, server_url: str, path: str = str(API_DEFINITION_PATH)
    ) -> None: ...
    def _build_api_url(self, server_url: str, site_id: str) -> str: ...
    def get_version_information(self) -> Optional[VersionObject]: ...
    def request(
        self,
        endpoint_name: str,
        no_default_headers: bool = False,
        data: Optional[str] = None,
        url_data: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        etag: Optional[str] = None,
        debug: bool = False,
        log_access: bool = False,
    ) -> Optional[DomainObject]: ...
    def __enter__(self) -> Optional["SamaApiClient"]: ...
    def __exit__(self, exc_type, exc_value, traceback) -> Literal[False]: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
