# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - API client Core - configuration
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

# SAMA API Client - Core API Functions
#
# This module contains the core API functions for the SAMA API Client.

# Import required modules

from pathlib import Path
from logging import INFO

# Constants
# Environment Variable Constants

ENV_FILE_NAME = ".env"  # The environment file name.

# The environment variable for the Check Mk automation user.
ENV_USER = "SAMA_AUTOMATION_USER"
# The environment variable for the Check Mk automation secret.
ENV_SECRET = "SAMA_AUTOMATION_SECRET"

# KEYRING Constants

KEYRING_SERVICE = "sama_api_client"  # The keyring service name.
KEYRING_USER = "sama_automation_user"  # The keyring user name.
KEYRING_SECRET = "sama_automation_secret"  # The keyring secret name.

# Logger constants

LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"  # The log format.
LOG_LEVEL = INFO  # The default log level.
LOGGER_NAME = "sama_api_client"  # The logger name.

# Define an API endpoint for the connect_endpoint property of the SamaApiClient class.

API_VERSION_ENDPOINT = "version"  # The API endpoint to test the connection.

# API Endpoint Constants

# The API endpoint definition file.
API_ENDPOINT_DEFINITION_FILE = "api_endpoints.json"

# The API endpoint definition full path.
API_DEFINITION_PATH = Path(__file__).parent / API_ENDPOINT_DEFINITION_FILE

API_BASE_URL = "/check_mk/api/1.0"  # The base URL for the Check Mk API, this version number is for Check Mk 2.1.0 and later.
# NOTE: The base url is subject to change if the Check Mk API changes in version 2.4.0 or later.

# Redacted string

REDACTED = "<:This is redacted for security reasons:>"

# Enable the API call on connect.
# This is to test the connection to the API
# when the client is created.
ENABLE_API_CALL_ON_CONNECT = False
