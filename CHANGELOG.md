# SAMA API Client - CHANGELOG

## 2.0.0 (2024-12-31)

This is a new major release of the SAMA API Client.
In effect it is a complete rewrite of the client, with new features.

## 2.0.0 (2025-01-03)

Version 2.0.0.alpha.6 is a bugfix release for the alpha version of the client.
Added debugging to the api_request function.
Added extra information for the HTTPError exception if it was raised.
Added access logging to the core.
Added headers argument to the api_request and request functions to override/append headers.
Added ETag property to the response object.
Added etag argument to the client.request function.
Added Status204 method to the domain object.
Added check for response code 204 in the response object in the client.request function.
