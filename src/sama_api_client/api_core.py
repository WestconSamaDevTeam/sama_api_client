# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - API client Core
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

# SAMA API Client - Core API Functions
#
# This module contains the core API functions for the SAMA API Client.

# Import required modules

import os
import keyring
import json

from logging import Logger
from logging import INFO
from logging import StreamHandler
from logging import Formatter
from logging import getLogger
from logging import DEBUG
from logging import ERROR
from logging import WARNING

from dotenv import load_dotenv

from typing import Optional, Literal

from requests import Session
from requests.exceptions import HTTPError
from requests.models import Response

from urllib.parse import urlencode
from urllib.parse import quote

from sama_api_client.api_endpoint import APIEndpoint
from sama_api_client.__about__ import __VERSION__

# Constants

__BASE_API_URL__ = "/check_mk/api/1.0"  # The base URL for the Check Mk API, this version number is for Check Mk 2.1.0 and later.
# NOTE: The base url is subject to change if the Check Mk API changes in version 2.4.0 or later.

# Environment Variable Constants

__ENV_FILE__ = ".env"  # The environment file name.

# The environment variable for the Check Mk automation user.
__ENV_USER__ = "SAMA_AUTOMATION_USER"
# The environment variable for the Check Mk automation secret.
__ENV_SECRET__ = "SAMA_AUTOMATION_SECRET"

# KEYRING Constants

__KEYRING_SERVICE__ = "sama_api_client"  # The keyring service name.
__KEYRING_USER__ = "sama_automation_user"  # The keyring user name.
__KEYRING_SECRET__ = "sama_automation_secret"  # The keyring secret name.

# Logger constants

__LOG_FORMAT__ = "%(asctime)s %(name)s %(levelname)s %(message)s"  # The log format.
__LOG_LEVEL__ = INFO  # The log level.
__LOGGER_NAME__ = "sama_api_client"  # The logger name.

# Define an API endpoint

__API_VERSION_ENDPOINT__ = "version"  # The API endpoint to test the connection.

__API_ENDPOINT_DEFINITION_FILE__ = (
    "api_endpoints.json"  # The API endpoint definition file.
)

# Define the API Core class


class SamaApiClientCore:
    """
    SAMA API Client Core is the base class for the SamaAPiClient class.
    It provides all the core functions for the SAMA API Client to communicate with the Check Mk 2.x REST API.

    This class contains the core functions for the SAMA API Client.
    """

    # Define the class constructor
    def __init__(
        self,
        site_id: str,
        server_url: str,
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
        self.site_id: str = site_id
        self.api_url: str = self._build_api_url(server_url, site_id)
        self.session: Session = Session()
        self.endpoints: list[APIEndpoint] = []

        # Set the class logger
        self.logger: Logger = self._init_logger()

        # Set the class headers
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._get_token()}",
        }

    # private functions

    def _build_api_url(self, server_url: str, site_id: str) -> str:
        """

        This method builds the API URL.

        :param server_url: The server URL.
        :param site_id: The site ID.

        :return: The API URL.

        """

        api_url = f"{server_url}/{site_id}{__BASE_API_URL__}"
        return api_url

    def _init_logger(self) -> Logger:
        """
        Initialize the logger.
        """
        logger: Logger = getLogger(__LOGGER_NAME__)
        logger.setLevel(__LOG_LEVEL__)
        logger.propagate = False
        logger.handlers.clear()
        handler: StreamHandler = StreamHandler()
        handler.setLevel(__LOG_LEVEL__)
        formatter: Formatter = Formatter(__LOG_FORMAT__)
        handler.setFormatter(formatter)
        return logger

    def _get_env_token(self) -> Optional[str]:
        """

        This method retrieves the token from the environment variables.

        :return: The token, or none if the token is not found.

        """
        # Load the environment variables from the .env file if it exists, this ensures that
        # it takes precedence over the system environment variables.
        load_dotenv(__ENV_FILE__)

        # Get the token from the environment variables
        user: Optional[str] = os.getenv(__ENV_USER__)
        if user is None:
            return None
        secret: Optional[str] = os.getenv(__ENV_SECRET__)
        if secret is None:
            return None
        return f"{user} {secret}"

    def _get_keyring_token(self) -> Optional[str]:
        """

        This method retrieves the token from the keyring.

        :return: The token, or none if the token is not found.

        """

        # Get the token from the keyring
        user: Optional[str] = keyring.get_password(
            __KEYRING_SERVICE__, __KEYRING_USER__
        )
        if user is None:
            return None
        secret: Optional[str] = keyring.get_password(
            __KEYRING_SERVICE__, __KEYRING_SECRET__
        )
        if secret is None:
            return None
        return f"{user} {secret}"

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
        params: Optional[dict] = None,
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

    def load_endpoints(self, path: str = __API_ENDPOINT_DEFINITION_FILE__) -> bool:
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
        endpoint_headers: Optional[dict],
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
            response: Response = self.session.get(
                f"{self.api_url}/{__API_VERSION_ENDPOINT__}",
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
        self.session.close()

    def api_request(
        self,
        endpoint_name: str,
        no_default_headers: bool = False,
        data: Optional[str] = None,
        url_data: Optional[str] = None,
        params: Optional[dict] = None,
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

        headers: dict = self.headers  # Set the headers
        if no_default_headers:
            headers = {}
        if endpoint.headers is not None:
            headers.update(endpoint.headers)

        # Make the API call
        try:
            if debug is True:
                print(f"API Request: {method} {api_url}")
                ho = headers.copy()
                ho["Authorization"] = "Bearer <:This is was redacted by my l33t :):>"
                print(f"Headers: {ho}")
                print(f"Data: {data}")
                print(f"URL Data: {url_data}")
                print(f"Params: {params}")
                print()
            if log_access:
                self.logger.info(f"API Request: {method} {api_url}")
                ho = headers.copy()
                ho["Authorization"] = "Bearer <:This is was redacted by my l33t :):>"
                self.logger.info(f"Headers: {ho}")
                self.logger.info(f"Data: {data}")
                self.logger.info(f"URL Data: {url_data}")
                self.logger.info(f"Params: {params}")
            response: Response = self.session.request(
                method, api_url, headers=headers, data=data
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
            ho = headers.copy()
            ho["Authorization"] = "Bearer <:This is was redacted by my l33t :):>"
            msg = f"HTTP Error: {e}\nRequest: {method} {api_url}\nHeaders: {ho}\nData: {data}\nURL Data: {url_data}\nParams: {params}\nReason: {response.reason}"
            self.logger.error(msg)
            if debug is True:
                print(msg)
                print()
            return None
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            return None

    # Context manager

    def __enter__(self) -> Optional["SamaApiClientCore"]:
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
        return f"SamaApiClientCore(site_id={self.site_id}, api_url={self.api_url})"

    def __repr__(self) -> str:
        return self.__str__()
