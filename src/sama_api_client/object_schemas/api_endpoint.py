# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - API Endpoint object schema
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

# The API endpoint module contains the API endpoint class and functions.
#
# An API endpoint consists of the following components:
#
# - API endpoint name      - an easy name to access the API endpoint
# - API endpoint path      - the API endpoint path
# - API endpoint method    - the API endpoint method
# - API endpoint headers   - the API endpoint headers if they are required in addition to the default headers


# Import required modules

from typing import Optional

# Define the API endpoint class


class APIEndpoint:
    """
    The API endpoint class contains the API endpoint components.
    """

    def __init__(
        self,
        name: str,
        path: str,
        method: str,
        headers: Optional[dict[str, str]] = None,
    ):
        """
        Initialize the API endpoint class.

        :param name: The API endpoint name.
        :param path: The API endpoint path.
        :param method: The API endpoint method.
        :param headers: The API endpoint headers.
        """
        self.name: str = name
        self.path: str = path
        self.method: str = method
        self.headers: Optional[dict[str, str]] = headers

    def __str__(self) -> str:
        """
        :return: The API endpoint as a string.
        """
        return f"ApiEndpoint(name={self.name}, path={self.path}, method={self.method})"

    def __repr__(self) -> str:
        """
        :return: The API endpoint representation.
        """
        return self.__str__()
