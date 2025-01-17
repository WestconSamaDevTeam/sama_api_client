# SAMA Api client

## Table of contents

- [SAMA Api client](#sama-api-client)
  - [Table of contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Check Mk Rest API Authentication](#check-mk-rest-api-authentication)
  - [REST API Client core - API class initialization](#rest-api-client-core---api-class-initialization)
  - [SAMA API Client core - logging](#sama-api-client-core---logging)
  - [REST API Client core - API endpoints](#rest-api-client-core---api-endpoints)
  - [SAMA API Client core - API requests](#sama-api-client-core---api-requests)
  - [SAMA API Client - SamaApiClient](#sama-api-client---samaapiclient)
  - [Demos](#demos)
  - [Installation](#installation)
  - [Conclusion](#conclusion)

## Introduction

The SAMA API client is a Python library that provides a simple way to interact with the Check Mk 2.x API.
The library is designed to be easy to use and easy to extend.

This library is built on top of the requests library, which is a popular library for making HTTP requests in Python.

It is a rewrite of the CheckmkAPIClient that used the RestApiClientCore for communicating with the Check Mk API.
The SamaApiClient is a single library that implements both the RestApiClientCore and the CheckmkAPIClient.
The the CheckmkAPIClient is renamed to SamaApiClient.
Where RestApiClientCore is used as the base class of the SamaApiClient.
It was refactored to become API agnostic. Its only function is to handle the communication with the REST API of a REST API server.

It is a known fact that Check Mk 2.x API is going to change coming version 2.3 and later of Check Mk , where in version 2.4
the previous versions of the API are going to be removed.

This library is designed to be easily extendible.
The CheckmkAPIClient implemented all supported API endpoints in the class as functions.
This library is designed to be more flexible and to allow the user to define the API endpoints separately.
In fact, it can even load a json file with the API endpoints without requiring any additional code.

The basic functionality of the SAMA API client is provided by the RestApiClientCore class.
This core class handles the communication with the REST API of the Check Mk server.
It is so flexible that it can be used even on its own as a generic API client for any REST API.

The SamaApiClient class inherits from the RestApiClientCore class and will provide additional
functionality that is specific to SAMA/Check Mk.

## Check Mk Rest API Authentication

To set up Bearer authentication for the Checkmk REST API, follow these steps:

Create or use an existing automation user in Checkmk:
Go to Setup > Users > Users in the Checkmk web interface.

Use the pre-configured 'automation' user or create a new one.

Ensure the user has the necessary permissions for your intended API actions.
Obtain the automation secret (password) for the chosen user
When making API requests, include the following header in each request:

```text
Authorization: Bearer username:secret
```

Replace 'username' with your automation user's name and 'secret' with the user's automation secret
Use this header in your API calls. For example, using curl

```bash
curl -H "Authorization: Bearer automation your_automation_secret" -H "Accept: application/json" https://your_checkmk_server/your_site/check_mk/api/1.0/domain/endpoint
```

Remember to replace 'your_automation_secret', 'your_checkmk_server', 'your_site', and the API endpoint with your specific values.
It's important to note that Bearer authentication is the recommended method for scripts and takes precedence over other authentication methods. Ensure that you use HTTPS for secure transmission of credentials.

## REST API Client core - API class initialization

From the previous chapter we learned how to authenticate with the Check Mk API, now we set up our SAMA API client class initialization with some the key components needed for this.

The key components are:

username: The username of the automation user, the automation user as defined in the previous chapter.
secret: The secret of the automation user, the secret as defined in the previous chapter.
site_id: The site id of the Check Mk site, the site id is the name of the site as defined in the Check Mk web interface.
url: The URL of the Check Mk api.

The URL of the Check Mk API is the base URL of the Check Mk server with the path to the API endpoint appended to it. The API base endpoint is /check_mk/api/1.0. Because this is a constant value, we define it as a constant in the client api core.
NOTE: Check Mk 2.4 and later may define a different version (2.0) of the API, in this case, the base endpoint will be /check_mk/api/2.0.
Because we define this in the constant, we can easily change the version of the API by changing the constant value.

The only part of the URL that changes is the base URL of the Check Mk server. This is the URL of the Check Mk server where the API is hosted. We define this as a parameter of the SAMA API client class.

Because we want to offer the option of using a keyring or environment variables to store the username and the secret of the automation user, we define the username and secret as optional parameters of the SAMA API client class.

The site_id and server_url are required parameters of the SAMA API client class.

For environment variables we provide the option that they are defined in a .env file or as environment variables in the system.
These variables are defined as constants in the client api core.

A further option that we offer for the credentials is to store them in the keyring. The keyring is a secure way to store credentials on the system. The keyring is a Python library that provides a simple way to store and retrieve credentials from the system keyring.

The order in which the credentials are used is as follows:
class init > keyring > .env file > environment variables.

The SAMA API client class initialization is as follows (provided you use the environment variables or keyring to store the credentials):

```python
from sama_api_client import RestApiClientCore

with RestApiClientCore(api_url='https://your_checkmk_server/site_id/check_mk/api/1.0', username='your_username', secret='your_secret') as client:
    if client is None:
        print('Could not authenticate with the Check Mk API')
        exit(1)
    # Do something with the client
```

The above method uses the so called context manager to handle the authentication with the Check Mk API. The context manager is a Python construct that allows you to define a setup and a teardown method for a class. The setup method is called when the context manager is entered and the teardown method is called when the context manager is exited.

This ensures that the connection to the API is set up and torn down correctly

For testing purposes this is ideal, but it may not be the best way to handle the connection to the API in a production environment. In a production environment you may want to handle the connection to the API in a different way.
To this end the connect and close functions are provided in the SAMA API client core:

```python
from sama_api_client import RestApiClientCore

client = RestApiClientCore(api_url='https://your_checkmk_server/site_id/check_mk/api/1.0')
if client.connect() is False:
    print('Could not authenticate with the Check Mk API')
    exit(1)
# Do something with the client
client.close()
```

The connect function calls the API endpoint to authenticate with the Check Mk API and get the version information.
This way we ensure that a connection is possible and that the API is available.
If for some reason the connection is not possible, the connect function returns False and the connection is not set up.
The connection function will also log the error message to the logger if an error has occurred.

## SAMA API Client core - logging

The SAMA API client core uses the Python logging module to log messages to the console by default.
The log format and the log level are defined as constants in the client api core.
The log level is set to INFO by default, but can be changed to DEBUG or ERROR if needed.
The log format is set to:

```text
%(asctime)s %(name)s %(levelname)s %(message)s
```

The log format can be changed if needed.

The log messages are logged to the console by default, but can be changed to log to a file if needed.
To change this use the following code:

```python
import logging

from sama_api_client import RestApiClientCore

logging.basicConfig(filename='sama_api_client.log', level=logging.INFO)
client = RestApiClientCore(api_url='https://your_checkmk_server/site_id/check_mk/api/1.0')
if client.connect() is False:
    print('Could not authenticate with the Check Mk API')
    exit(1)
# Do something with the client
client.close()
```

The logging.basicConfig function is used to set up the logging to log to a file.
The filename parameter is used to specify the name of the log file.
The level parameter is used to specify the log level.

## REST API Client core - API endpoints

The REST API client core provides a simple way to interact with any REST API.
The Check Mk API is a RESTful API that provides a way to interact with the Check Mk server.
For more details on the Check Mk API see the Check Mk API documentation that is accessible through the Check Mk web interface.

The REST API client core provides a way to interact with any REST API by defining the API endpoints through a registry function.

An API endpoint consists of the following components:

- the name
- the path
- the method
- optional headers

These are the parameters that are needed to create an APIEndpoint object.

The APIEndpoint object is a simple object that contains the name, the path, the method, and the optional headers of the API endpoint.

It can be created as follows:

```python
from sama_api_client.object_schemas import APIEndpoint

api_endpoint = APIEndpoint(name='Version', path='version', method='GET', headers={})
```

While the headers are optional, it is good practice to define them as an empty dictionary.

The RestApiClientCore class allows you to add individual API endpoints to the API registry using the add_endpoint function.

The add_endpoint function takes an APIEndpoint object as a parameter and adds it to the API registry.

```python
from sama_api_client import RestApiClientCore
from sama_api_client.object_schemas import APIEndpoint

api_endpoint = APIEndpoint(name='Version', path='version', method='GET', headers={})

client = RestApiClientCore(api_url='https://your_checkmk_server/site_id/check_mk/api/1.0')
client.add_endpoint(api_endpoint)
```

While this method works for adding individual API endpoints to the API registry, it is not the most efficient way to add multiple API endpoints to the API endpoint registry.

For this reason the RestApiClientCore class provides a way to register individual API endpoints using the register_endpoints function.
This takes care of initializing the APIEndpoint objects and adding them to the API registry.

The register_endpoint function takes the same parameters as the APIEndpoint object.

```python
from sama_api_client import RestApiClientCore

client = RestApiClientCore(api_url='https://your_checkmk_server/site_id/check_mk/api/1.0')

client.register_endpoint(name='Version', path='version', method='GET', headers={})
client.register_endpoint(name='Hosts', path='hosts', method='GET', headers={})

```

This reduces the amount of code needed to add multiple API endpoints to the API registry.
However, it is still not the most efficient way to add multiple API endpoints to the API registry in case there are many API endpoints to add.

For this reason the RestApiClientCore class provides a way to register multiple API endpoints using a json file.
The format of the json file needs to match the format of the APIEndpoint object.
It should look like this:

```json
[
    {
        "name": "Version",
        "path": "version",
        "method": "GET",
        "headers": {}
    },
    {
        "name": "Hosts",
        "path": "hosts",
        "method": "GET",
        "headers": {}
    }
]
```

The json file can be loaded using the load_endpoints function.

```python
from sama_api_client import RestApiClientCore

client = RestApiClientCore(api_url='https://your_checkmk_server/site_id/check_mk/api/1.0')
if client.load_endpoints('api_endpoints.json') is False:
    print('Could not load the API endpoints')
    exit(1)
```

This will load the API endpoints from the json file and add them to the API registry.
There is a default path name for the load_endpoints function, so you may call it without the path parameter.
Still it is good practice to define the path to the json file.

## SAMA API Client core - API requests

Now that all the API endpoints are registered in the API registry, we can start making API requests to the Check Mk API.
The api_request function can be used to make API requests to the Check Mk API.
This function will return a Response object from the requests library.
It will contain the response from the Check Mk API.
If any error occurs, the function will return None. Any errors that happened will be logged.

The following code demonstrates how to make an API request to the Check Mk API using the api_request function:

```python
from sama_api_client import RestApiClientCore

client = RestApiClientCore(api_url='https://your_checkmk_server/site_id/check_mk/api/1.0')
client.register_endpoint(name='Version', path='version', method='GET', headers={})
if client.connect() is False:
    print('Could not authenticate with the Check Mk API')
    exit(1)
response = client.api_request('Version')
if response is None:
    print('Could not make the API request')
    exit(1)
print(response.json())
```

This will make an API request to the Check Mk API using the Version API endpoint.
The expected response is a json object that contains the version information of the Check Mk server.
It should look similar to this:

```json
{
    'site': 'samadev_test',
    'group': '',
    'rest_api': {'revision': '0'},
    'versions': {
        'apache': [2, 4, 57],
        'checkmk': '2.1.0p48.cme',
        'python': '3.9.16 (main, Jul 25 2023, 22:30:53) \n[GCC 12.2.0]',
        'mod_wsgi': [4, 9, 4],
        'wsgi': [1, 0]
    },
    'edition': 'cme',
    'demo': False
}
```

## SAMA API Client - SamaApiClient

The SamaApiClient class is a subclass of the RestApiClientCore class.
It provides additional functionality that is specific to SAMA/Check Mk.

While you can use the functions of the RestApiClientCore class to interact with the Check Mk API even if you instantiate the SamaApiClient class, the SamaApiClient class provides a translation layer that makes it easier to interact with the Check Mk API.

The Check Mk REST API returns (on most endpoints) a json object that is named the Domain object.
The Domain object is a dictionary that contains the data of the API endpoint.

In the sama_api_client.object_schemas.domain_object module we define the DomainObject class to make it
easier to interact with the output of the Check Mk API.
So instead of having to deal with the raw output of a request performed by the requests library, you can use the DomainObject class to interact with the data.

The original API on which the SamaApiClient is based implemented a separate function for each API endpoint.
This is no longer the case, all API endpoints are now defined in the API registry and can be accessed using the request function of the SamaApiClient class.

The only exception to this is the version endpoint, which is a special case and is implemented as a separate function.
The reason for this is that this endpoint doesn't return a Domain object, but a Version object.
This version object is defined in the sama_api_client.object_schemas.version_object module.

## Demos

The tests folder contains the client_demo.py and core_demo.py files.
These files demonstrate how to use the SAMA API client core and the SAMA API client.
For simplicity both demos request and display the same information.
The difference is that the SamaApiCoreClient returns only a requests.Response object, while the SamaApiClient returns a DomainObject object for all normal API endpoints, and a VersionObject object for the version endpoint.

## Installation

To install the SAMA API client on your system, we assume that you have set up your development system according to the instructions on the Sama Dev Team Sharepoint.

The SAMA API client is available on our GitHub account as a private repository.
To install the SAMA API client, you need to clone the repository to your system.
The simplest is using our sdt utility.

```bash
sdt get sama_api_client
```

This will clone the repository to your system, to use it you need to use the make utility several times.

```bash
make init_env
```

This will prepare the virtual environment for the SAMA API client.
You need to activate it:

```bash
source env/bin/activate
```

Now you can install the SAMA API client:

```bash
make
```

This will build the SAMA API client and install it in the active virtual environment.

You can now run the demos in the tests folder, or use the SAMA API client in your own projects by installing the .whl file in the dist folder in your own projects virtual environment.

For convenience i have added two make commands that can run the demos for you:

```bash
make core_demo
```

This will run the core_demo.py file in the tests folder.

```bash
make client_demo
```

This will run the client_demo.py file in the tests folder.

## Conclusion

The SAMA API client is a Python library that provides a simple way to interact with the Check Mk 2.x API.
It is designed to be easy to use and easy to extend.

The library is built on top of the requests library, which is a popular library for making HTTP requests in Python.
It is also a combination of two older projects, the Check Mk API client and the Rest API client.
Where the Rest API Client is now the RestApiClientCore and the Check Mk API client is the SamaApiClient.

Where the older projects did a more exact implementation and had a function for each supported API endpoint, the new SAMA API client is more flexible and allows the user to define the API endpoints in a separate file, and call each endpoint by name.
