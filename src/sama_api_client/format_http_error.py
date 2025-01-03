# -*- coding: utf-8 -*-
#
# Product:   SAMA API Client - HTTPError print function
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# Date:      2025-01-03
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

# Import required modules

import json
from requests.exceptions import HTTPError


def print_http_error(http_error: HTTPError):
    try:
        error_data = json.loads(http_error.response.text)
        print("Error Details:")
        print(f"  Title: {error_data.get('title', 'N/A')}")
        print(f"  Status: {error_data.get('status', 'N/A')}")
        print(f"  Detail: {error_data.get('detail', 'N/A')}")

        if "fields" in error_data:
            print("  Field Errors:")
            for field, errors in error_data["fields"].items():
                print(f"    {field}:")
                for error in errors:
                    print(f"      - {error}")
    except json.JSONDecodeError:
        print(f"Failed to parse error response. Raw text: {http_error.response.text}")
    except AttributeError:
        print(f"Unexpected error structure. Error: {http_error}")


def format_http_error_for_logging(http_error: HTTPError) -> str:
    try:
        error_data = json.loads(http_error.response.text)

        # Start with basic error information
        error_msg = f"HTTP Error {error_data.get('status', 'N/A')}: {error_data.get('title', 'Unknown Error')}\n"
        error_msg += f"Detail: {error_data.get('detail', 'No details provided')}\n"

        # Add field-specific errors if present
        if "fields" in error_data:
            error_msg += "Field Errors:\n"
            for field, errors in error_data["fields"].items():
                error_msg += f"  {field}: {', '.join(errors)}\n"

        return error_msg.strip()  # Remove trailing newline
    except json.JSONDecodeError:
        return f"Failed to parse error response. Raw text: {http_error.response.text}"
    except AttributeError:
        return f"Unexpected error structure. Error: {http_error}"
