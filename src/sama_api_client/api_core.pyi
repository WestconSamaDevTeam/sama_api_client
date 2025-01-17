# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - REST API client Core - type stub
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

from typing import Optional, Literal, Dict, Any
from logging import Logger
from requests import Session, Response
from sama_api_client.object_schemas.api_endpoint import APIEndpoint
from sama_api_client.configuration import API_DEFINITION_PATH

class RestApiClientCore:
    api_url: str
    user: Optional[str]
    secret: Optional[str]
    session: Session
    endpoints: list[APIEndpoint]
    logger: Logger
    headers: Dict[str, str]
    _connect_endpoint: str

    def __init__(
        self, api_url: str, user: Optional[str] = None, secret: Optional[str] = None
    ) -> None: ...
    @property
    def connection_endpoint(self) -> str: ...
    @connection_endpoint.setter
    def connection_endpoint(self, value: str) -> None: ...
    def _init_logger(self) -> Logger: ...
    def _get_env_token(self) -> Optional[str]: ...
    def _get_keyring_token(self) -> Optional[str]: ...
    def _get_token(self) -> Optional[str]: ...
    def _build_api_call_url(
        self,
        endpoint_path: str,
        url_data: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> str: ...
    def _get_endpoint(self, endpoint_name: str) -> Optional[APIEndpoint]: ...
    def get_version(self) -> str: ...
    def load_endpoints(self, path: str = str(API_DEFINITION_PATH)) -> bool: ...
    def register_endpoint(
        self,
        endpoint_name: str,
        endpoint_path: str,
        method: str,
        endpoint_headers: Optional[Dict[str, str]],
    ) -> None: ...
    def add_endpoint(self, endpoint: APIEndpoint) -> None: ...
    def connect(self) -> bool: ...
    def close(self) -> None: ...
    def api_request(
        self,
        endpoint_name: str,
        no_default_headers: bool = False,
        data: Optional[str] = None,
        url_data: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        log_access: bool = False,
        debug: bool = False,
    ) -> Optional[Response]: ...
    def __enter__(self) -> Optional["RestApiClientCore"]: ...
    def __exit__(self, exc_type, exc_value, traceback) -> Literal[False]: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
