# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - client demo
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

# This module contains demo code to showcase the SAMA API client.

# Import required modules

from sama_api_client.api_client import SamaApiClient

from rich import print


def main() -> None:

    client: SamaApiClient = SamaApiClient(
        site_id="samadev_test",
        server_url="http://localhost:1024",
        path="../src/sama_api_client/api_endpoints.json",
    )
    sama_version_information = client.get_version_information()
    all_folders = client.request("GetAllFolders")

    if sama_version_information is None:
        print("Could not retrieve the version information")
        exit(1)

    if all_folders is None:
        print("Could not retrieve the folders")
        exit(1)

    print(sama_version_information)
    print(all_folders)


if __name__ == "__main__":
    main()
