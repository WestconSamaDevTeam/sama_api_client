# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - REST API client Core
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

# SAMA API Client - REST API client Core
#
# This module contains the API agnostic REST API client core class.
#
# The core class provides the basic functionality to communicate with a REST API.
#

# Import required modules

import os
import keyring
import json

from logging import Logger
from logging import INFO
from logging import StreamHandler
from logging import Formatter
from logging import getLogger

from dotenv import load_dotenv

from typing import Optional, Literal, Any

from requests import Session
from requests.exceptions import HTTPError
from requests.models import Response

from urllib.parse import urlencode
from urllib.parse import quote

from sama_api_client.object_schemas.api_endpoint import APIEndpoint
from sama_api_client.__about__ import __VERSION__
from sama_api_client.format_http_error import print_http_error
from sama_api_client.format_http_error import format_http_error_for_logging

from sama_api_client.configuration import LOGGER_NAME
from sama_api_client.configuration import LOG_LEVEL
from sama_api_client.configuration import LOG_FORMAT
from sama_api_client.configuration import ENV_FILE_NAME
from sama_api_client.configuration import ENV_USER
from sama_api_client.configuration import ENV_SECRET
from sama_api_client.configuration import KEYRING_SERVICE
from sama_api_client.configuration import KEYRING_USER
from sama_api_client.configuration import KEYRING_SECRET
from sama_api_client.configuration import REDACTED
from sama_api_client.configuration import API_VERSION_ENDPOINT
from sama_api_client.configuration import API_DEFINITION_PATH
from sama_api_client.configuration import ENABLE_API_CALL_ON_CONNECT

# Define the API Core class


class RestApiClientCore:
    """

    REST API Client Core is an API agnostic base class.
    It provides all the functions for the an API Client to communicate with a REST API.
    API endpoints can be added/registered using functions or loaded from a JSON file.

    """

    # Define the class constructor
    def __init__(
        self,
        api_url: str,
        user: Optional[str] = None,
        secret: Optional[str] = None,
    ):
        """

        This method initializes the SAMA API Client Core class.

        :param user: The Check Mk automation user.
        :param secret: The Check Mk automation secret.
        :param site_id: The Check Mk site ID, the name of the site.
        :param api_url: The SAMA API URL.

        """

        # Set the class variables
        self.user: Optional[str] = user
        self.secret: Optional[str] = secret
        self.api_url: str = api_url
        self.session: Session = Session()
        self.endpoints: list[APIEndpoint] = []
        self._connect_endpoint: str = API_VERSION_ENDPOINT

        # Set the class logger
        self.logger: Logger = self._init_logger()

        # Set the class headers
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._get_token()}",
            "Accept": "application/json",
        }

    # properties

    @property
    def connection_endpoint(self) -> str:
        """

        This property returns the connection endpoint.

        :return: The connection endpoint.

        """
        return self._connect_endpoint

    @connection_endpoint.setter
    def connection_endpoint(self, value: str) -> None:
        """

        This property sets the connection endpoint.

        :param value: The connection endpoint.

        """
        self._connect_endpoint = value

    # private functions

    def _init_logger(self) -> Logger:
        """
        Initialize the logger.
        """
        logger: Logger = getLogger(LOGGER_NAME)
        logger.setLevel(LOG_LEVEL)
        logger.propagate = False
        logger.handlers.clear()
        handler: StreamHandler = StreamHandler()
        handler.setLevel(LOG_LEVEL)
        formatter: Formatter = Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        return logger

    def _get_env_token(self) -> Optional[str]:
        """

        This method retrieves the token from the environment variables.

        :return: The token, or none if the token is not found.

        """
        # Load the environment variables from the .env file if it exists, this ensures that
        # it takes precedence over the system environment variables.
        load_dotenv(ENV_FILE_NAME)

        # Get the token from the environment variables
        user: Optional[str] = os.getenv(ENV_USER)
        if user is None:
            return None
        secret: Optional[str] = os.getenv(ENV_SECRET)
        if secret is None:
            return None
        return f"{user} {secret}"

    def _get_keyring_token(self) -> Optional[str]:
        """

        This method retrieves the token from the keyring.

        :return: The token, or none if the token is not found.

        """

        # Get the token from the keyring
        try:
            user: Optional[str] = keyring.get_password(KEYRING_SERVICE, KEYRING_USER)
            if user is None:
                return None
            secret: Optional[str] = keyring.get_password(
                KEYRING_SERVICE, KEYRING_SECRET
            )
            if secret is None:
                return None
            return f"{user} {secret}"
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            return None

    def _get_token(self) -> Optional[str]:
        """

        This method retrieves the token from the keyring.

        :return: The token.

        rule of precedence:
        class init > keyring > .env file > environment variables

        """

        # Get the token from the class init
        if self.user is not None and self.secret is not None:
            return f"{self.user} {self.secret}"

        # Get the token from the keyring if it exists
        keyring_token: Optional[str] = self._get_keyring_token()
        if keyring_token is not None:
            return keyring_token

        # Get the token from the environment variables
        env_token: Optional[str] = self._get_env_token()
        if env_token is not None:
            return env_token

        # Return None if the token is not found
        return None

    def _build_api_call_url(
        self,
        endpoint_path: str,
        url_data: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> str:
        """

        This method builds the API URL to call an endpoint.

        :param endpoint_path: The path of the endpoint.
        :param url_data: The optional URL data.
        :param params: The optional parameters.

        :return: The API URL.

        """
        api_url: str = f"{self.api_url}/{endpoint_path}"

        if url_data is not None:
            safe_url_data: str = quote(url_data)
            api_url = f"{api_url}/{safe_url_data}"

        if params is None:
            return api_url

        if params is not None:
            api_url = f"{api_url}?{urlencode(params)}"

        return api_url

    def _get_endpoint(self, endpoint_name: str) -> Optional[APIEndpoint]:
        """

        This method retrieves an API endpoint by name.

        :param endpoint_name: The name of the endpoint.

        :return: The API endpoint, or None if the endpoint is not found.

        """

        # Find the endpoint by name
        return next((e for e in self.endpoints if e.name == endpoint_name), None)

    # public functions

    def get_version(self) -> str:
        """

        This method retrieves the version of the SAMA API Client.

        :return: The version of the SAMA API Client.

        """

        # Return the version
        return __VERSION__

    def load_endpoints(self, path: str = str(API_DEFINITION_PATH)) -> bool:
        """

        This method loads the API endpoints from the API endpoint definition file.

        :return: True if the endpoints are loaded successfully, False otherwise.

        """

        # Load the API endpoints
        try:
            with open(path, "r") as file:
                endpoint_json = json.load(file)
                self.endpoints = [
                    APIEndpoint(
                        name=e["name"],
                        path=e["path"],
                        method=e["method"],
                        headers=e["headers"],
                    )
                    for e in endpoint_json
                ]
                return True
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            return False

    def register_endpoint(
        self,
        endpoint_name: str,
        endpoint_path: str,
        method: str,
        endpoint_headers: Optional[dict[str, str]],
    ) -> None:
        """

        This method registers an endpoint.

        :param endpoint_name: The name of the endpoint.
        :param endpoint_path: The path of the endpoint.
        :param method: The method of the endpoint.
        :param endpoint_headers: The headers of the endpoint, optional.

        """

        # Register the endpoint
        self.endpoints.append(
            APIEndpoint(
                name=endpoint_name,
                path=endpoint_path,
                method=method,
                headers=endpoint_headers,
            )
        )

    def add_endpoint(self, endpoint: APIEndpoint) -> None:
        """

        This method adds an endpoint.

        :param endpoint: The endpoint to add.

        """

        # Add the endpoint
        self.endpoints.append(endpoint)

    def connect(self) -> bool:
        """

        This method tests the connection to the Check Mk API.

        :return: True if the connection is successful, False otherwise.

        Raises:
            HTTPError if the connection is not successful.
            Exception if there is an unhandled exception.


        """

        # Test the connection to the Check Mk API
        try:
            if ENABLE_API_CALL_ON_CONNECT is True:
                response: Response = self.session.get(
                    f"{self.api_url}/{self._connect_endpoint}",
                    headers=self.headers,
                )
                response.raise_for_status()
            return True
        except HTTPError as e:
            self.logger.error(f"HTTPError: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            return False

    def close(self) -> None:
        """

        This method closes the session.

        """

        # Close the session
        if self.session is not None:
            self.session.close()

    def api_request(
        self,
        endpoint_name: str,
        no_default_headers: bool = False,
        data: Optional[str] = None,
        url_data: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
        log_access: bool = False,
        debug: bool = False,
    ) -> Optional[Response]:
        """

        This method makes an API call to an endpoint.

        :param endpoint_name: The name of the endpoint.
        :param no_default_headers: True if the default headers should not be used, False otherwise.
        :param data: The optional data for the body of the request.
        :param url_data: The optional URL data.
        :param params: The optional parameters.
        :param log_access: True if the access should be logged, False otherwise. Default is False.
        :param debug: True if the request and response should be printed, False otherwise. Default is False.

        :return: The response, or None if the response is not successful.

        """

        # Get the endpoint
        endpoint: Optional[APIEndpoint] = self._get_endpoint(endpoint_name)
        if endpoint is None:
            self.logger.error(f"Endpoint not found: {endpoint_name}")
            return None

        # Build the API URL
        api_url: str = self._build_api_call_url(endpoint.path, url_data, params)

        method: str = endpoint.method

        out_headers: dict[str, str] = self.headers  # Set the default headers
        if no_default_headers:
            out_headers = {}
        # override default headers with endpoint headers
        if endpoint.headers is not None:
            out_headers.update(endpoint.headers)
        # override default headers with headers that are provided in the call
        if headers is not None:
            out_headers.update(headers)

        # Make the API call
        try:
            if debug is True:
                print(f"API Request: {method} {api_url}")
                ho = out_headers.copy()
                ho["Authorization"] = f"Bearer {REDACTED}"
                print(f"Headers: {ho}")
                print(f"Data: {data}")
                print(f"URL Data: {url_data}")
                print(f"Params: {params}")
                print()
            if log_access:
                self.logger.info(f"API Request: {method} {api_url}")
                ho = out_headers.copy()
                ho["Authorization"] = f"Bearer {REDACTED}"
                self.logger.info(f"Headers: {ho}")
                self.logger.info(f"Data: {data}")
                self.logger.info(f"URL Data: {url_data}")
                self.logger.info(f"Params: {params}")
            response: Response = self.session.request(
                method, api_url, headers=out_headers, data=data
            )
            response.raise_for_status()
            if debug is True:
                print(f"API Response: {response.status_code}")
                print(f"Response Headers: {response.headers}")
                print(f"Response Data: {response.text}")
                print()
            if log_access:
                self.logger.info(f"API Response: {response.status_code}")
                self.logger.info(f"Response Headers: {response.headers}")
                self.logger.info(f"Response Data: {response.text}")
            return response
        except HTTPError as e:
            if debug is True:
                print_http_error(e)
            msg = format_http_error_for_logging(e)
            self.logger.error(msg)
            return None
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            return None

    # Context manager

    def __enter__(self) -> Optional["RestApiClientCore"]:
        try:
            self.connect()
            return self
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            return None

    def __exit__(self, exc_type, exc_value, traceback) -> Literal[False]:
        if exc_type is not None:
            self.logger.error(f"Exception: {exc_type}: {exc_value}")
            self.logger.error(f"Traceback: {traceback}")
            return False
        self.close()
        return False

    # String representation

    def __str__(self) -> str:
        return f"RestApiClientCore(api_url={self.api_url})"

    def __repr__(self) -> str:
        return self.__str__()
