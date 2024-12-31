# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - Version object schema
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

# Import required modules

from pydantic import BaseModel

# Example of the version object as it is returned by the Check Mk REST API:
#
# {
#    "site": "samadev_test",
#    "group": "",
#    "rest_api": {"revision": "0"},
#    "versions": {
#        "apache": [2, 4, 57],
#        "checkmk": "2.1.0p48.cme",
#        "python": "3.9.16 (main, Jul 25 2023, 22:30:53) \n[GCC 12.2.0]",
#        "mod_wsgi": [4, 9, 4],
#        "wsgi": [1, 0],
#    },
#    "edition": "cme",
#    "demo": False,
# }
#
# As you can see the returned data is very different from a DomainObject. This is why we need a separate schema for the version information.
#


class VersionObject(BaseModel):
    site: str
    group: str
    rest_api: dict
    versions: dict
    edition: str
    demo: bool
