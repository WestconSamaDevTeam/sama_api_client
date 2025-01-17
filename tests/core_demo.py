# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - core demo
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

# This module contains demo code to showcase the SAMA API client core.

# Import required modules

from sama_api_client.api_core import RestApiClientCore  # type: ignore

from requests.models import Response

from typing import Optional

from rich import print


def main() -> None:

    client: RestApiClientCore = RestApiClientCore(
        api_url="http://localhost:1024/samadev_test/check_mk/api/v1"
    )
    if client.load_endpoints() is False:
        print("Could not load the API endpoints")
        exit(1)
    if client.connect() is False:
        print("Could not authenticate with the Check Mk API")
        exit(1)
    sama_version_information: Optional[Response] = client.api_request("Version")
    all_folders: Optional[Response] = client.api_request("GetAllFolders")
    client.close()

    if sama_version_information is None:
        print("Could not retrieve the version information")
        exit(1)
    if all_folders is None:
        print("Could not retrieve the folders")
        exit(1)

    print()
    print("SAMA API Version Information")
    print("----------------------------")
    print(sama_version_information.json())
    print()
    print("All Folders")
    print("-----------")
    print(all_folders.json())


if __name__ == "__main__":
    main()
