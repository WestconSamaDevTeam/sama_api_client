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

## 2.0.0.alpha.7 (2025-01-08)

Added "Accept": "application/json", to the default headers in the api_core.py module, api_core class.
Added __REDACTED__ constant to the api_core.py module this is used to redact sensitive information in the logs.

## 2.0.0.alpha.8 (2025-01-16)

Moved the _build_api_url function from the api_core.py module to the api_client.py module.
Removed the site_id parameter from api_core class.
Renamed SamaApiClientCore to RestApiClientCore, because it is the generic/core class that gets inherited to make it specific to SAMA.
RestApiClientCore renamed server_url to api_url.
Moved all the constants from the api_core.py module to the configuration.py module.
Created typing stub for the RestApiClientCore class.
Created typing stub for the SamaApiClient class.
Created typing stub for the version_object class.
Created typing stub for the domain_object class.
Created typing stub for the link_object class.
Moved api_endpoint.py module to the object_schemas directory.
Created typing stub for the ApiEndpoint class.
Updated SamaApiClient init function, path argument gets a default value of str(__API_DEFINITION_PATH__). This is the path to the API definition file. Which is a JSON file that contains the API endpoints and their schemas. The path is calculated from Path(__file__).parent / "api_definition.json", hence the requirement of the str() cast on the Path object because the init argument is a str.
Created Sama API Client 2025.docx documentation.
Fixed pyproject.toml file format to comply with the standards.
Updated the README.md file with the new features and changes.

## 2.0.0.alpha.9 (2025-01-17)

Added the ENABLE_API_CALL_ON_CONNECT constant to the configuration.py module. This is used to enable or disable the API call on connect. The default value is False.
This will speed up the client initialization process, by not making an API call on connect.
Added the ENABLE_API_CALL_ON_CONNECT argument to the RestApiClient init function. This is used to enable or disable the API call on connect.

## 2.0.0.beta.1 (2025-02-03)

Fixed an issue with _get_keyring_token in the core, it could raise an exception if the keyring module was not installed or the proper credentials weren't set inside the keyring.
Now it returns None if the keyring module is not installed or no credentials were found.
